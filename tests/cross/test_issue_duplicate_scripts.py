from __future__ import annotations

import argparse
import importlib.util
import io
import itertools
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
MODULE_COUNTER = itertools.count()


def load_module(script_name: str):
    path = ROOT / "scripts" / script_name
    module_name = f"test_{path.stem}_{next(MODULE_COUNTER)}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_agent_message(text: str) -> dict:
    return {
        "kind": "MessageEvent",
        "source": "agent",
        "llm_message": {"content": [{"type": "text", "text": text}]},
    }


def iso_timestamp(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_list_open_issues_filters_by_duplicate_candidate_label(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")
    requested_paths: list[str] = []
    responses = [
        [
            {"number": 1},
            {"number": 2, "pull_request": {"url": "https://example.test/pr/2"}},
        ],
        [{"number": 3}],
        [],
    ]

    def fake_request_json(path: str, *, method: str = "GET", body=None):
        requested_paths.append(path)
        return responses.pop(0)

    monkeypatch.setattr(module, "request_json", fake_request_json)

    assert module.list_open_issues("OpenHands/agent-sdk") == [
        {"number": 1},
        {"number": 3},
    ]
    assert requested_paths == [
        "/repos/OpenHands/agent-sdk/issues?state=open&labels=duplicate-candidate&per_page=100&page=1",
        "/repos/OpenHands/agent-sdk/issues?state=open&labels=duplicate-candidate&per_page=100&page=2",
        "/repos/OpenHands/agent-sdk/issues?state=open&labels=duplicate-candidate&per_page=100&page=3",
    ]


def test_list_issue_comments_paginates(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")
    requested_paths: list[str] = []
    responses = [[{"id": 1}], [{"id": 2}], []]

    def fake_request_json(path: str, *, method: str = "GET", body=None):
        requested_paths.append(path)
        return responses.pop(0)

    monkeypatch.setattr(module, "request_json", fake_request_json)

    assert module.list_issue_comments("OpenHands/agent-sdk", 7) == [
        {"id": 1},
        {"id": 2},
    ]
    assert requested_paths == [
        "/repos/OpenHands/agent-sdk/issues/7/comments?per_page=100&page=1",
        "/repos/OpenHands/agent-sdk/issues/7/comments?per_page=100&page=2",
        "/repos/OpenHands/agent-sdk/issues/7/comments?per_page=100&page=3",
    ]


def test_list_comment_reactions_paginates(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")
    requested_paths: list[str] = []
    responses = [[{"id": 1}], [{"id": 2}], []]

    def fake_request_json(path: str, *, method: str = "GET", body=None):
        requested_paths.append(path)
        return responses.pop(0)

    monkeypatch.setattr(module, "request_json", fake_request_json)

    assert module.list_comment_reactions("OpenHands/agent-sdk", 99) == [
        {"id": 1},
        {"id": 2},
    ]
    assert requested_paths == [
        "/repos/OpenHands/agent-sdk/issues/comments/99/reactions?per_page=100&page=1",
        "/repos/OpenHands/agent-sdk/issues/comments/99/reactions?per_page=100&page=2",
        "/repos/OpenHands/agent-sdk/issues/comments/99/reactions?per_page=100&page=3",
    ]


def test_list_helpers_raise_on_non_list_payloads(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")

    monkeypatch.setattr(module, "request_json", lambda *args, **kwargs: {"bad": True})

    with pytest.raises(
        RuntimeError, match="Expected list response while listing open issues"
    ):
        module.list_open_issues("OpenHands/agent-sdk")
    with pytest.raises(
        RuntimeError, match="Expected list response while listing comments"
    ):
        module.list_issue_comments("OpenHands/agent-sdk", 7)
    with pytest.raises(
        RuntimeError, match="Expected list response while listing reactions"
    ):
        module.list_comment_reactions("OpenHands/agent-sdk", 9)


def test_ensure_page_limit_raises():
    module = load_module("auto_close_duplicate_issues.py")

    with pytest.raises(RuntimeError, match="Exceeded pagination limit"):
        module.ensure_page_limit(module.MAX_PAGES + 1, "open issues")


def test_parse_timestamp_reports_invalid_values():
    module = load_module("auto_close_duplicate_issues.py")

    with pytest.raises(ValueError, match="Failed to parse timestamp"):
        module.parse_timestamp("invalid")


def test_parse_timestamp_accepts_microseconds():
    module = load_module("auto_close_duplicate_issues.py")

    parsed = module.parse_timestamp("2026-04-21T21:10:11.123456Z")

    assert parsed == datetime(2026, 4, 21, 21, 10, 11, 123456, tzinfo=UTC)


def test_github_headers_requires_token(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")

    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    with pytest.raises(
        RuntimeError, match="GITHUB_TOKEN environment variable is required"
    ):
        module.github_headers()


def test_auto_close_parse_args_rejects_invalid_repository(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")

    monkeypatch.setattr(
        module.sys,
        "argv",
        ["auto_close_duplicate_issues.py", "--repository", "bad/repo/name"],
    )

    with pytest.raises(SystemExit, match="2"):
        module.parse_args()

    captured = capsys.readouterr()
    assert "Invalid repository format: bad/repo/name" in captured.err


def test_auto_close_request_json_reports_urlerror(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")

    monkeypatch.setattr(module, "github_headers", lambda: {})
    monkeypatch.setattr(
        module.urllib.request,
        "urlopen",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            module.urllib.error.URLError("boom")
        ),
    )

    with pytest.raises(RuntimeError, match="GET /test failed"):
        module.request_json("/test")


def test_auto_close_request_json_reports_httperror(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")

    monkeypatch.setattr(module, "github_headers", lambda: {})
    error = module.urllib.error.HTTPError(
        url="https://example.test/test",
        code=403,
        msg="Forbidden",
        hdrs=None,
        fp=io.BytesIO(b'{"message":"denied"}'),
    )
    monkeypatch.setattr(
        module.urllib.request,
        "urlopen",
        lambda *args, **kwargs: (_ for _ in ()).throw(error),
    )

    with pytest.raises(RuntimeError, match=r"GET /test failed with HTTP 403: .*denied"):
        module.request_json("/test")


def test_auto_close_request_json_reports_invalid_json(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")
    monkeypatch.setattr(module, "github_headers", lambda: {})

    class DummyResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b"not-json"

    monkeypatch.setattr(
        module.urllib.request, "urlopen", lambda *args, **kwargs: DummyResponse()
    )

    with pytest.raises(RuntimeError, match="Failed to parse JSON from /test"):
        module.request_json("/test")


def test_is_non_bot_comment_filters_github_bots():
    module = load_module("auto_close_duplicate_issues.py")

    assert (
        module.is_non_bot_comment({"user": {"id": 1, "type": "User", "login": "enyst"}})
        is True
    )
    assert (
        module.is_non_bot_comment(
            {"user": {"id": 2, "type": "Bot", "login": "renovate[bot]"}}
        )
        is False
    )
    assert (
        module.is_non_bot_comment(
            {"user": {"id": 3, "type": "User", "login": "all-hands-bot"}}
        )
        is False
    )
    assert (
        module.is_non_bot_comment(
            {"user": {"id": 4, "type": "User", "login": "dependabot[bot]"}}
        )
        is False
    )
    assert module.is_non_bot_comment({"user": None}) is False


def test_has_reaction_from_user_ignores_missing_user_ids():
    module = load_module("auto_close_duplicate_issues.py")
    reactions = [
        {"user": None, "content": "-1"},
        {"user": {"id": 42}, "content": "-1"},
    ]

    assert module.user_id_from_item({"user": None}) is None
    assert module.has_reaction_from_user(reactions, None, "-1") is False
    assert module.has_reaction_from_user(reactions, 42, "-1") is True
    assert module.has_reaction_from_user(reactions, 42, "+1") is False


def test_is_non_bot_comment_requires_string_login():
    module = load_module("auto_close_duplicate_issues.py")

    assert module.is_non_bot_comment({"user": {"id": 7, "login": None}}) is False


def test_extract_duplicate_metadata_and_veto_helpers():
    module = load_module("auto_close_duplicate_issues.py")

    assert module.extract_duplicate_metadata(
        "<!-- openhands-duplicate-check canonical=42 auto-close=true -->"
    ) == (42, True)
    assert module.extract_duplicate_metadata("plain comment") == (None, False)
    assert (
        module.has_veto_note(
            [{"body": f"noticed\n{module.DUPLICATE_VETO_MARKER}\nthanks"}]
        )
        is True
    )
    assert module.has_veto_note([{"body": "plain comment"}]) is False


def test_issue_has_label_handles_string_and_object_labels():
    module = load_module("auto_close_duplicate_issues.py")

    issue = {
        "labels": [
            module.DUPLICATE_CANDIDATE_LABEL,
            {"name": "bug"},
        ]
    }

    assert module.issue_has_label(issue, module.DUPLICATE_CANDIDATE_LABEL) is True
    assert module.issue_has_label(issue, "bug") is True
    assert module.issue_has_label(issue, "enhancement") is False


def test_find_latest_auto_close_comment_prefers_newest_timestamp():
    module = load_module("auto_close_duplicate_issues.py")
    comments = [
        {
            "body": "<!-- openhands-duplicate-check canonical=10 auto-close=true -->",
            "created_at": "2026-04-20T00:00:00Z",
            "id": 1,
        },
        {
            "body": "<!-- openhands-duplicate-check canonical=11 auto-close=true -->",
            "created_at": "2026-04-19T00:00:00Z",
            "id": 2,
        },
    ]

    latest_comment, canonical_issue = module.find_latest_auto_close_comment(comments)

    assert latest_comment == comments[0]
    assert canonical_issue == 10


def test_find_latest_auto_close_comment_returns_latest_candidate():
    module = load_module("auto_close_duplicate_issues.py")
    comments = [
        {"body": "plain comment"},
        {
            "body": "<!-- openhands-duplicate-check canonical=10 auto-close=false -->",
            "id": 1,
            "created_at": "2026-04-18T00:00:00Z",
        },
        {
            "body": "<!-- openhands-duplicate-check canonical=11 auto-close=true -->",
            "id": 2,
            "created_at": "2026-04-19T00:00:00Z",
        },
        {
            "body": "<!-- openhands-duplicate-check canonical=12 auto-close=true -->",
            "id": 3,
            "created_at": "2026-04-20T00:00:00Z",
        },
    ]

    latest_comment, canonical_issue = module.find_latest_auto_close_comment(comments)

    assert latest_comment == comments[-1]
    assert canonical_issue == 12


def test_close_issue_propagates_comment_failure(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")
    calls: list[tuple[str, str]] = []

    def fake_request_json(path: str, *, method: str = "GET", body=None):
        calls.append((method, path))
        if method == "POST" and path.endswith("/comments"):
            raise RuntimeError("comment failed")
        return {}

    def fake_remove_candidate_label(
        repository: str, issue_number: int, *, dry_run: bool
    ):
        calls.append(("REMOVE_LABEL", f"{repository}#{issue_number}:{dry_run}"))
        return True

    monkeypatch.setattr(module, "request_json", fake_request_json)
    monkeypatch.setattr(module, "remove_candidate_label", fake_remove_candidate_label)

    with pytest.raises(RuntimeError, match="comment failed"):
        module.close_issue_as_duplicate("OpenHands/agent-sdk", 123, 45, dry_run=False)

    assert calls == [
        ("POST", "/repos/OpenHands/agent-sdk/issues/123/comments"),
    ]


def test_dry_run_helpers_skip_api_calls(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")

    monkeypatch.setattr(
        module,
        "request_json",
        lambda *args, **kwargs: pytest.fail(
            "request_json should not run in dry-run mode"
        ),
    )

    assert module.remove_candidate_label("OpenHands/agent-sdk", 1, dry_run=True) is True
    assert module.post_veto_note("OpenHands/agent-sdk", 1, dry_run=True) is True

    monkeypatch.setattr(
        module,
        "remove_candidate_label",
        lambda *args, **kwargs: pytest.fail(
            "remove_candidate_label should not run in dry-run close path"
        ),
    )
    assert (
        module.close_issue_as_duplicate("OpenHands/agent-sdk", 1, 2, dry_run=True)
        is None
    )


def test_close_issue_as_duplicate_removes_label_on_success(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")
    calls: list[tuple[str, str]] = []

    def fake_request_json(path: str, *, method: str = "GET", body=None):
        calls.append((method, path))
        return {}

    def fake_remove_candidate_label(
        repository: str, issue_number: int, *, dry_run: bool
    ):
        calls.append(("REMOVE_LABEL", f"{repository}#{issue_number}:{dry_run}"))
        return True

    monkeypatch.setattr(module, "request_json", fake_request_json)
    monkeypatch.setattr(module, "remove_candidate_label", fake_remove_candidate_label)

    module.close_issue_as_duplicate("OpenHands/agent-sdk", 123, 45, dry_run=False)

    assert calls == [
        ("POST", "/repos/OpenHands/agent-sdk/issues/123/comments"),
        ("PATCH", "/repos/OpenHands/agent-sdk/issues/123"),
        ("REMOVE_LABEL", "OpenHands/agent-sdk#123:False"),
    ]


def test_keep_open_due_to_newer_comments_removes_candidate_label(monkeypatch):
    module = load_module("auto_close_duplicate_issues.py")
    calls: list[tuple[str, int, bool]] = []

    def fake_remove_candidate_label(
        repository: str, issue_number: int, *, dry_run: bool
    ):
        calls.append((repository, issue_number, dry_run))
        return True

    monkeypatch.setattr(module, "remove_candidate_label", fake_remove_candidate_label)

    result = module.keep_open_due_to_newer_comments(
        "OpenHands/agent-sdk",
        {"labels": [{"name": "duplicate-candidate"}]},
        123,
        dry_run=False,
    )

    assert result == {
        "issue_number": 123,
        "action": "kept-open",
        "reason": "newer-comment-after-duplicate-notice",
        "label_removed": True,
    }
    assert calls == [("OpenHands/agent-sdk", 123, False)]


def test_auto_close_main_honors_author_veto(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")
    now = datetime.now(UTC)
    old_timestamp = iso_timestamp(now - timedelta(days=5))
    issue = {
        "number": 123,
        "created_at": old_timestamp,
        "labels": [{"name": module.DUPLICATE_CANDIDATE_LABEL}],
        "user": {"id": 7},
    }
    comments = [
        {
            "id": 11,
            "body": "<!-- openhands-duplicate-check canonical=45 auto-close=true -->",
            "created_at": old_timestamp,
        }
    ]
    reactions = [{"user": {"id": 7}, "content": "-1"}]
    removed: list[tuple[str, int, bool]] = []
    veto_notes: list[tuple[str, int, bool]] = []

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(module, "list_open_issues", lambda repository: [issue])
    monkeypatch.setattr(
        module, "list_issue_comments", lambda repository, number: comments
    )
    monkeypatch.setattr(
        module, "list_comment_reactions", lambda repository, comment_id: reactions
    )
    monkeypatch.setattr(
        module,
        "remove_candidate_label",
        lambda repository, issue_number, *, dry_run: removed.append(
            (repository, issue_number, dry_run)
        )
        or True,
    )
    monkeypatch.setattr(
        module,
        "post_veto_note",
        lambda repository, issue_number, *, dry_run: veto_notes.append(
            (repository, issue_number, dry_run)
        )
        or True,
    )
    monkeypatch.setattr(
        module,
        "close_issue_as_duplicate",
        lambda *args, **kwargs: pytest.fail("close_issue_as_duplicate should not run"),
    )

    assert module.main() == 0

    summary = json.loads(capsys.readouterr().out)
    assert summary == {
        "repository": "OpenHands/agent-sdk",
        "results": [
            {
                "issue_number": 123,
                "action": "kept-open",
                "reason": "author-thumbed-down-duplicate-comment",
                "label_removed": True,
                "veto_note_posted": True,
                "author_thumbs_up": False,
            }
        ],
    }
    assert removed == [("OpenHands/agent-sdk", 123, False)]
    assert veto_notes == [("OpenHands/agent-sdk", 123, False)]


def test_auto_close_main_closes_old_duplicate(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")
    now = datetime.now(UTC)
    old_timestamp = iso_timestamp(now - timedelta(days=5))
    issue = {
        "number": 123,
        "created_at": old_timestamp,
        "labels": [{"name": module.DUPLICATE_CANDIDATE_LABEL}],
        "user": {"id": 7},
    }
    comments = [
        {
            "id": 11,
            "body": "<!-- openhands-duplicate-check canonical=45 auto-close=true -->",
            "created_at": old_timestamp,
        }
    ]
    closed: list[tuple[str, int, int, bool]] = []

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(module, "list_open_issues", lambda repository: [issue])
    monkeypatch.setattr(
        module, "list_issue_comments", lambda repository, number: comments
    )
    monkeypatch.setattr(
        module, "list_comment_reactions", lambda repository, comment_id: []
    )
    monkeypatch.setattr(
        module,
        "close_issue_as_duplicate",
        lambda repository,
        issue_number,
        canonical_issue_number,
        *,
        dry_run: closed.append(
            (repository, issue_number, canonical_issue_number, dry_run)
        ),
    )

    assert module.main() == 0

    summary = json.loads(capsys.readouterr().out)
    assert summary == {
        "repository": "OpenHands/agent-sdk",
        "results": [
            {
                "issue_number": 123,
                "action": "closed-as-duplicate",
                "canonical_issue_number": 45,
                "author_thumbs_up": False,
            }
        ],
    }
    assert closed == [("OpenHands/agent-sdk", 123, 45, False)]


def test_auto_close_main_continues_after_close_failure(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")
    now = datetime.now(UTC)
    old_timestamp = iso_timestamp(now - timedelta(days=5))
    issues = [
        {
            "number": 123,
            "created_at": old_timestamp,
            "labels": [{"name": module.DUPLICATE_CANDIDATE_LABEL}],
            "user": {"id": 7},
        },
        {
            "number": 124,
            "created_at": old_timestamp,
            "labels": [{"name": module.DUPLICATE_CANDIDATE_LABEL}],
            "user": {"id": 8},
        },
    ]
    comments = [
        {
            "id": 11,
            "body": "<!-- openhands-duplicate-check canonical=45 auto-close=true -->",
            "created_at": old_timestamp,
        }
    ]
    closed: list[int] = []

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(module, "list_open_issues", lambda repository: issues)
    monkeypatch.setattr(
        module, "list_issue_comments", lambda repository, number: comments
    )
    monkeypatch.setattr(
        module, "list_comment_reactions", lambda repository, comment_id: []
    )

    def fake_close_issue_as_duplicate(
        repository: str,
        issue_number: int,
        canonical_issue_number: int,
        *,
        dry_run: bool,
    ) -> None:
        if issue_number == 123:
            raise RuntimeError("comment failed")
        closed.append(issue_number)

    monkeypatch.setattr(
        module, "close_issue_as_duplicate", fake_close_issue_as_duplicate
    )

    assert module.main() == 0

    captured = capsys.readouterr()
    summary = json.loads(captured.out)
    assert summary == {
        "repository": "OpenHands/agent-sdk",
        "results": [
            {
                "issue_number": 123,
                "action": "failed",
                "error": "comment failed",
            },
            {
                "issue_number": 124,
                "action": "closed-as-duplicate",
                "canonical_issue_number": 45,
                "author_thumbs_up": False,
            },
        ],
    }
    assert "Error processing issue #123: comment failed" in captured.err
    assert closed == [124]


def test_auto_close_main_skips_malformed_issue_data(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(
        module, "list_open_issues", lambda repository: [{"number": 123}]
    )
    monkeypatch.setattr(module, "list_issue_comments", lambda repository, number: [])

    assert module.main() == 0

    summary = json.loads(capsys.readouterr().out)
    assert summary == {"repository": "OpenHands/agent-sdk", "results": []}


def test_auto_close_main_skips_malformed_duplicate_comment(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")
    now = datetime.now(UTC)
    old_timestamp = iso_timestamp(now - timedelta(days=5))
    issue = {
        "number": 123,
        "created_at": old_timestamp,
        "labels": [{"name": module.DUPLICATE_CANDIDATE_LABEL}],
        "user": {"id": 7},
    }
    comments = [
        {
            "body": "<!-- openhands-duplicate-check canonical=45 auto-close=true -->",
            "created_at": old_timestamp,
        }
    ]

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(module, "list_open_issues", lambda repository: [issue])
    monkeypatch.setattr(
        module, "list_issue_comments", lambda repository, number: comments
    )
    monkeypatch.setattr(
        module,
        "close_issue_as_duplicate",
        lambda *args, **kwargs: pytest.fail("close_issue_as_duplicate should not run"),
    )

    assert module.main() == 0

    summary = json.loads(capsys.readouterr().out)
    assert summary == {"repository": "OpenHands/agent-sdk", "results": []}


def test_auto_close_main_skips_non_numeric_issue_number(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")
    now = datetime.now(UTC)

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(
        module,
        "list_open_issues",
        lambda repository: [
            {"number": "oops", "created_at": iso_timestamp(now - timedelta(days=5))}
        ],
    )

    assert module.main() == 0

    summary = json.loads(capsys.readouterr().out)
    assert summary == {"repository": "OpenHands/agent-sdk", "results": []}


def test_auto_close_main_skips_non_numeric_comment_id(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")
    now = datetime.now(UTC)
    old_timestamp = iso_timestamp(now - timedelta(days=5))
    issue = {
        "number": 123,
        "created_at": old_timestamp,
        "labels": [{"name": module.DUPLICATE_CANDIDATE_LABEL}],
        "user": {"id": 7},
    }
    comments = [
        {
            "id": "oops",
            "body": "<!-- openhands-duplicate-check canonical=45 auto-close=true -->",
            "created_at": old_timestamp,
        }
    ]

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(module, "list_open_issues", lambda repository: [issue])
    monkeypatch.setattr(
        module, "list_issue_comments", lambda repository, number: comments
    )
    monkeypatch.setattr(
        module,
        "close_issue_as_duplicate",
        lambda *args, **kwargs: pytest.fail("close_issue_as_duplicate should not run"),
    )

    assert module.main() == 0

    summary = json.loads(capsys.readouterr().out)
    assert summary == {"repository": "OpenHands/agent-sdk", "results": []}


def test_auto_close_main_removes_label_when_newer_comment_exists(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")
    now = datetime.now(UTC)
    old_timestamp = iso_timestamp(now - timedelta(days=5))
    newer_timestamp = iso_timestamp(now - timedelta(days=4))
    issue = {
        "number": 123,
        "created_at": old_timestamp,
        "labels": [{"name": module.DUPLICATE_CANDIDATE_LABEL}],
        "user": {"id": 7},
    }
    comments = [
        {
            "id": 11,
            "body": "<!-- openhands-duplicate-check canonical=45 auto-close=true -->",
            "created_at": old_timestamp,
        },
        {
            "id": 12,
            "body": "new info",
            "created_at": newer_timestamp,
            "user": {"id": 8, "type": "User", "login": "someone"},
        },
    ]
    keep_open_calls: list[tuple[str, int, bool]] = []

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(module, "list_open_issues", lambda repository: [issue])
    monkeypatch.setattr(
        module, "list_issue_comments", lambda repository, number: comments
    )
    monkeypatch.setattr(
        module, "list_comment_reactions", lambda repository, comment_id: []
    )
    monkeypatch.setattr(
        module,
        "keep_open_due_to_newer_comments",
        lambda repository, issue_arg, issue_number, *, dry_run: keep_open_calls.append(
            (repository, issue_number, dry_run)
        )
        or {"issue_number": issue_number, "action": "kept-open"},
    )
    monkeypatch.setattr(
        module,
        "close_issue_as_duplicate",
        lambda *args, **kwargs: pytest.fail("close_issue_as_duplicate should not run"),
    )

    assert module.main() == 0

    summary = json.loads(capsys.readouterr().out)
    assert summary == {
        "repository": "OpenHands/agent-sdk",
        "results": [{"issue_number": 123, "action": "kept-open"}],
    }
    assert keep_open_calls == [("OpenHands/agent-sdk", 123, False)]


def test_auto_close_main_ignores_newer_bot_comments(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")
    now = datetime.now(UTC)
    old_timestamp = iso_timestamp(now - timedelta(days=5))
    newer_timestamp = iso_timestamp(now - timedelta(days=4))
    issue = {
        "number": 123,
        "created_at": old_timestamp,
        "labels": [{"name": module.DUPLICATE_CANDIDATE_LABEL}],
        "user": {"id": 7},
    }
    comments = [
        {
            "id": 11,
            "body": "<!-- openhands-duplicate-check canonical=45 auto-close=true -->",
            "created_at": old_timestamp,
        },
        {
            "id": 12,
            "body": "status update",
            "created_at": newer_timestamp,
            "user": {"id": 8, "type": "User", "login": "all-hands-bot"},
        },
    ]
    closed: list[tuple[str, int, int, bool]] = []

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(module, "list_open_issues", lambda repository: [issue])
    monkeypatch.setattr(
        module, "list_issue_comments", lambda repository, number: comments
    )
    monkeypatch.setattr(
        module, "list_comment_reactions", lambda repository, comment_id: []
    )
    monkeypatch.setattr(
        module,
        "close_issue_as_duplicate",
        lambda repository,
        issue_number,
        canonical_issue_number,
        *,
        dry_run: closed.append(
            (repository, issue_number, canonical_issue_number, dry_run)
        ),
    )
    monkeypatch.setattr(
        module,
        "keep_open_due_to_newer_comments",
        lambda *args, **kwargs: pytest.fail(
            "keep_open_due_to_newer_comments should not run"
        ),
    )

    assert module.main() == 0

    summary = json.loads(capsys.readouterr().out)
    assert summary == {
        "repository": "OpenHands/agent-sdk",
        "results": [
            {
                "issue_number": 123,
                "action": "closed-as-duplicate",
                "canonical_issue_number": 45,
                "author_thumbs_up": False,
            }
        ],
    }
    assert closed == [("OpenHands/agent-sdk", 123, 45, False)]


def test_auto_close_main_ignores_newer_deleted_user_comments(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")
    now = datetime.now(UTC)
    old_timestamp = iso_timestamp(now - timedelta(days=5))
    newer_timestamp = iso_timestamp(now - timedelta(days=4))
    issue = {
        "number": 123,
        "created_at": old_timestamp,
        "labels": [{"name": module.DUPLICATE_CANDIDATE_LABEL}],
        "user": {"id": 7},
    }
    comments = [
        {
            "id": 11,
            "body": "<!-- openhands-duplicate-check canonical=45 auto-close=true -->",
            "created_at": old_timestamp,
        },
        {
            "id": 12,
            "body": "orphaned comment",
            "created_at": newer_timestamp,
            "user": None,
        },
    ]
    closed: list[tuple[str, int, int, bool]] = []

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(module, "list_open_issues", lambda repository: [issue])
    monkeypatch.setattr(
        module, "list_issue_comments", lambda repository, number: comments
    )
    monkeypatch.setattr(
        module, "list_comment_reactions", lambda repository, comment_id: []
    )
    monkeypatch.setattr(
        module,
        "close_issue_as_duplicate",
        lambda repository,
        issue_number,
        canonical_issue_number,
        *,
        dry_run: closed.append(
            (repository, issue_number, canonical_issue_number, dry_run)
        ),
    )

    assert module.main() == 0

    summary = json.loads(capsys.readouterr().out)
    assert summary["results"][0]["action"] == "closed-as-duplicate"
    assert closed == [("OpenHands/agent-sdk", 123, 45, False)]


def test_auto_close_main_skips_recent_duplicate_comments(monkeypatch, capsys):
    module = load_module("auto_close_duplicate_issues.py")
    now = datetime.now(UTC)
    issue = {
        "number": 123,
        "created_at": iso_timestamp(now - timedelta(days=30)),
        "labels": [{"name": module.DUPLICATE_CANDIDATE_LABEL}],
        "user": {"id": 7},
    }
    comments = [
        {
            "id": 11,
            "body": "<!-- openhands-duplicate-check canonical=45 auto-close=true -->",
            "created_at": iso_timestamp(now - timedelta(days=1)),
        }
    ]

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(module, "list_open_issues", lambda repository: [issue])
    monkeypatch.setattr(
        module, "list_issue_comments", lambda repository, number: comments
    )
    monkeypatch.setattr(
        module, "list_comment_reactions", lambda repository, comment_id: []
    )
    monkeypatch.setattr(
        module,
        "close_issue_as_duplicate",
        lambda *args, **kwargs: pytest.fail("close_issue_as_duplicate should not run"),
    )

    assert module.main() == 0

    assert json.loads(capsys.readouterr().out) == {
        "repository": "OpenHands/agent-sdk",
        "results": [],
    }


def test_auto_close_main_ignores_newer_comments_with_invalid_timestamps(
    monkeypatch, capsys
):
    module = load_module("auto_close_duplicate_issues.py")
    now = datetime.now(UTC)
    old_timestamp = iso_timestamp(now - timedelta(days=5))
    issue = {
        "number": 123,
        "created_at": old_timestamp,
        "labels": [{"name": module.DUPLICATE_CANDIDATE_LABEL}],
        "user": {"id": 7},
    }
    comments = [
        {
            "id": 11,
            "body": "<!-- openhands-duplicate-check canonical=45 auto-close=true -->",
            "created_at": old_timestamp,
        },
        {
            "id": 12,
            "body": "human but malformed",
            "created_at": "not-a-timestamp",
            "user": {"id": 8, "type": "User", "login": "enyst"},
        },
    ]
    closed: list[tuple[str, int, int, bool]] = []

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            repository="OpenHands/agent-sdk", close_after_days=3, dry_run=False
        ),
    )
    monkeypatch.setattr(module, "list_open_issues", lambda repository: [issue])
    monkeypatch.setattr(
        module, "list_issue_comments", lambda repository, number: comments
    )
    monkeypatch.setattr(
        module, "list_comment_reactions", lambda repository, comment_id: []
    )
    monkeypatch.setattr(
        module,
        "close_issue_as_duplicate",
        lambda repository,
        issue_number,
        canonical_issue_number,
        *,
        dry_run: closed.append(
            (repository, issue_number, canonical_issue_number, dry_run)
        ),
    )

    assert module.main() == 0

    captured = capsys.readouterr()
    assert "Ignoring newer comment with invalid timestamp" in captured.err
    assert json.loads(captured.out)["results"][0]["action"] == "closed-as-duplicate"
    assert closed == [("OpenHands/agent-sdk", 123, 45, False)]
