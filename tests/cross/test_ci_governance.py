"""Exercise the real CI gate and workflow resource-governance contracts."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import TypedDict

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
SCOPES = ("python", "typescript", "server", "examples", "storage", "security")
CHECKS = (
    "lint",
    "docstrings",
    "deprecations",
    "settings",
    "rest-api",
    "versions",
    "security",
    "python-tests",
    "typescript",
    "endpoint-audit",
    "integration",
    "server",
    "example-docs",
    "example-numbers",
    "storage",
)


def _workflow(name):
    # BaseLoader preserves the YAML `on` key instead of coercing it to True.
    return yaml.load((WORKFLOWS / name).read_text(), Loader=yaml.BaseLoader)


def _gate(results, event="pull_request"):
    script = _workflow("sdk-validation.yml")["jobs"]["gate"]["steps"][0]["run"]
    script = script.split("<<'PYCODE'\n", 1)[1].rsplit("\nPYCODE", 1)[0]
    return subprocess.run(
        [sys.executable, "-c", script],
        env={**os.environ, "RESULTS": json.dumps(results), "GITHUB_EVENT_NAME": event},
        capture_output=True,
        text=True,
        timeout=5,
    ).returncode


class CheckResult(TypedDict):
    result: str
    outputs: dict[str, str]


def _results(selected=True) -> dict[str, CheckResult]:
    results: dict[str, CheckResult] = {
        name: {"result": "success", "outputs": {}} for name in CHECKS
    }
    results["plan"] = {
        "result": "success",
        "outputs": {"validate": "true", **dict.fromkeys(SCOPES, str(selected).lower())},
    }
    return results


@pytest.mark.parametrize("check", CHECKS)
@pytest.mark.parametrize("result", ("failure", "cancelled", "skipped"))
def test_selected_checks_cannot_be_bypassed(check, result):
    results = _results()
    results[check]["result"] = result
    assert _gate(results) != 0


@pytest.mark.parametrize("event", ("pull_request", "merge_group", "workflow_dispatch"))
def test_successful_selected_checks_pass(event):
    assert _gate(_results(), event) == 0


def test_docs_and_exact_merge_reuse_allow_only_expected_skips():
    results = _results(selected=False)
    for check in CHECKS:
        if check not in ("lint", "versions"):
            results[check]["result"] = "skipped"
    assert _gate(results) == 0
    results["lint"]["result"] = "skipped"
    assert _gate(results) != 0
    results["versions"]["result"] = "skipped"
    results["plan"]["outputs"]["validate"] = "false"
    assert _gate(results, "push") == 0
    results["plan"]["result"] = "cancelled"
    assert _gate(results, "push") != 0


@pytest.mark.parametrize("flag", ("validate", *SCOPES))
def test_missing_planning_outputs_fail_closed(flag):
    results = _results()
    del results["plan"]["outputs"][flag]
    assert _gate(results) != 0


def test_source_checks_have_one_automatic_entry_point():
    controller = _workflow("sdk-validation.yml")
    assert controller["on"]["push"]["branches"] == ["main"]
    assert set(controller["on"]["pull_request"]["types"]) == {
        "opened",
        "reopened",
        "synchronize",
    }
    assert "merge_group" in controller["on"]
    assert controller["concurrency"]["cancel-in-progress"] == "true"
    evidence = controller["jobs"]["plan"]["steps"][-1]
    assert evidence["with"]["overwrite"] == "true"
    assert set(controller["permissions"].values()) == {"read"}
    assert set(controller["jobs"]["gate"]["needs"]) == {"plan", *CHECKS}
    for name in CHECKS:
        job = controller["jobs"][name]
        assert "secrets" not in job
        called = _workflow(Path(job["uses"]).name)
        assert "workflow_call" in called["on"]
        assert not {
            "push",
            "pull_request",
            "pull_request_target",
            "schedule",
        }.intersection(called["on"])
    for file in WORKFLOWS.glob("*.yml"):
        if file.name != "sdk-validation.yml":
            assert "push" not in _workflow(file.name)["on"], file.name


def test_controller_and_standalone_integration_build_exactly_once():
    controller = _workflow("sdk-validation.yml")
    assert controller["jobs"]["integration"]["with"]["reuse_build"] == "true"
    workflow = _workflow("typescript-client-integration-tests.yml")
    integration = workflow["jobs"]["integration-test"]["steps"]
    build = [s for s in integration if s.get("run") == "npm run build"]
    assert len(build) == 1 and "!inputs.reuse_build" in build[0]["if"]
    live = next(
        s for s in integration if s.get("name") == "Run LLM-backed integration tests"
    )
    assert "!inputs.reuse_build" in live["if"]
    assert "default_branch" in live["if"]
    smoke = workflow["jobs"]["smoke-test"]["steps"]
    assert not any(s.get("run") == "npm run build" for s in smoke)
    assert any(
        s.get("uses", "").startswith("actions/download-artifact@") for s in smoke
    )


def test_dependabot_groups_without_disabling_or_delaying_security_updates():
    config = yaml.load(
        (ROOT / ".github/dependabot.yml").read_text(), Loader=yaml.BaseLoader
    )
    updates = config["updates"]
    assert {u["package-ecosystem"] for u in updates} == {"github-actions", "uv", "npm"}
    assert len({u["schedule"]["day"] for u in updates}) == 3
    for update in updates:
        assert update["open-pull-requests-limit"] == "1"
        assert not any(key in update for key in ("ignore", "allow", "target-branch"))
        assert update["schedule"]["interval"] == "weekly"
        groups = list(update["groups"].values())
        assert {g["applies-to"] for g in groups} == {
            "version-updates",
            "security-updates",
        }
        assert all(g["patterns"] == ["*"] for g in groups)
        assert all("update-types" not in g for g in groups)


def test_publication_and_paid_agents_do_not_start_from_dependency_labels():
    for name in (
        "server.yml",
        "release-binaries.yml",
        "pypi-release.yml",
        "typescript-client-npm-publish.yml",
        "typescript-client-github-packages-publish.yml",
        "integration-runner.yml",
        "run-examples.yml",
        "todo-management.yml",
    ):
        assert set(_workflow(name)["on"]) == {"workflow_dispatch"}, name
    binary = _workflow("server-validation.yml")["jobs"]["build-binary-and-test"]
    assert binary["strategy"]["max-parallel"] == "2"
    upstream = _workflow("version-bump-prs.yml")["jobs"]
    for name in ("create-version-bump-prs", "bump-cloud-chart"):
        assert "github.repository_owner == 'OpenHands'" in upstream[name]["if"]
