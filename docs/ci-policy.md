# Praxis SDK CI policy

`SDK Validation` is the sole source-validation entry point. Its stable `SDK CI`
check fails when a selected check fails, is cancelled, or is unexpectedly skipped.
Required checks use job conditions, rather than workflow path filters, so a
documentation-only PR still receives a completed gate.

| Event | Validation |
| --- | --- |
| PR opened, reopened, or updated | Lint and version policy; relevant Python, server, TypeScript, example, storage and dependency checks |
| Push to `main` | Full validation unless the exact Git tree has successful, latest CI evidence from the merged PR |
| Push to a feature branch | Validation belongs to its PR; opening the PR and later pushes to it invoke the controller |
| Merge queue | Validation of the merge group's combined tree |
| Manual `SDK Validation` | Full validation |
| PR title, description or review changes | Lightweight description/review checks; source tests do not restart |
| Dependabot labels | No optional example, integration, evaluation or TODO runs |
| Publication | Explicit main-branch dispatch, separate from PR checks |

Unknown files, embedded prompts, Python packages, root dependencies and CI
changes select all runtime layers. TypeScript-only changes select TypeScript
unit tests, production-dependency audit, API tooling, deterministic integration
and pinned-image smoke tests. Documentation-only changes still run lint and
the PR version policy. Python dependency changes exercise consumers across layers.

The merge reuse rule checks the associated merged PR, its current head, the
latest successful run of this controller and its artifact provenance, including
the exact tested tree. Tree equality supports ordinary merge and squash commits;
missing/expired artifacts, API errors, changed trees, unsuccessful runs and
unrecognized merge provenance fall back to full validation. Rebase merges can
therefore run validation again when GitHub cannot establish that provenance.
An earlier run is never used in place of a newer failed or queued run.

New commits cancel obsolete CI for the same PR. Test jobs run in three lanes,
and packaging/publication matrices have `max-parallel: 2`. These are per-run
limits, not a reservation of organization-wide runner slots. Shared dependency
changes retain all Python test suites; the controller owns the path decisions.
The TypeScript build is compiled once and its artifact is reused by integration
and smoke jobs; the production npm audit runs once at the stricter moderate level.

PR source validation has a read-only token, persists no checkout credentials,
inherits no repository secrets, and never publishes packages. Deterministic
integration uses dummy LLM credentials. Real LLM integration is explicitly
dispatched on `main`; manual agent workflows likewise operate on `main`, not
untrusted PR branches. API and coverage reports remain in summaries/artifacts;
REST widening reports identify when a maintainer must add `release-note-required`.
Optional live examples/integration runs are not implied by the deterministic gate.

Dependabot groups version and security updates separately. Routine version
updates allow one open PR per ecosystem (three in total), staggered across Monday,
Tuesday and Wednesday at 06:00 UTC. Security updates stay enabled and grouped;
their PR limit is controlled separately by GitHub, not by the version-update limit.
Existing individual Dependabot PRs and previously queued runs are not removed by
this configuration. The npm runtime-pin updater is weekly. Daily upstream issue
auto-close scheduling and upstream docs/evaluation dispatches are disabled for
Praxiss-Lab; manual issue tooling remains available.

## Repository settings required for enforcement

The repository currently has no main protection or ruleset. Configure an active
ruleset for `main` in Settings > Rules > Rulesets:

- Require a pull request and at least one approving review.
- Require code-owner review, dismiss approvals after new commits, and require
  approval of the most recent reviewable push.
- Require `SDK CI`, `unresolved-review-threads` and `Validate PR description`
  checks, with GitHub Actions as the expected source.
- Require branches to be up to date (or use the supported merge queue).
- Require conversation resolution; block force pushes and branch deletion.
- Keep the bypass list empty unless an explicitly managed emergency process is needed.

`CODEOWNERS` assigns CI and dependency governance to `@Emilio-01-T`. It only
enforces approval when the ruleset requires code-owner review. Preserve the
read-only default Actions token and do not send write tokens/secrets to fork PRs.
Publisher environments may additionally require a human reviewer and main-only
deployment branches. Repository-admin settings cannot be installed through the
current connector and must be set in GitHub.

An approving review must come from another eligible maintainer; a PR author
cannot approve their own PR. For a solo-maintainer repository, enforce the PR
and CI requirements first and enable mandatory approvals when another reviewer
is available.

Agent Server image publication defaults to `ghcr.io/praxiss-lab/agent-server`.
Dispatch `Agent Server` from `main`, supplying the existing `release_tag` to
produce versioned images. Once that run passes, dispatch the release-artifact
workflow from `main` with the same tag; its Docker checks target those images.
Publishing all binary platforms is required before release assets are uploaded.

## Local verification

```sh
node --test .github/scripts/ci-policy.test.cjs
actionlint -shellcheck= -pyflakes=
uv run pre-commit run --files .github/workflows/sdk-validation.yml
```

The policy tests cover scopes, mismatched provenance, direct pushes, missing
artifacts and newer unsuccessful runs. Actual Python, binary, Docker and client
checks run on GitHub; local configuration tests do not replace them.
