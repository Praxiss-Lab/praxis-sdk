# Praxis SDK CI policy

`SDK Validation` is the sole source-validation entry point. Its stable `SDK CI`
check fails when a selected check fails, is cancelled, or is unexpectedly skipped.
Required checks use job conditions, rather than workflow path filters, so a
documentation-only PR still receives a completed gate.

| Event | Validation |
| --- | --- |
| PR opened, reopened, or updated | Lint and version policy; relevant Python, server, TypeScript, example, storage and dependency checks |
| Push to `main` | Full validation unless the exact Git tree has successful, latest CI evidence from the merged PR or the exact merge-group commit |
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
the exact tested tree. GitHub may return an empty `pull_requests` list on a run;
in that case the head SHA selects the candidate and the artifact must still
prove the repository, PR number, run and tested tree. Successful merge-group
runs may also be reused when their head commit and artifact tree match the
main push exactly. Tree equality supports ordinary merge and squash commits;
missing/expired artifacts, API errors, changed trees, unsuccessful runs and
unrecognized merge provenance fall back to full validation. Rebase merges can
therefore run validation again when GitHub cannot establish that provenance.
An earlier run is never used in place of a newer failed or queued run.

New commits cancel obsolete CI for the same PR. Test jobs run in three lanes,
and packaging/publication matrices have `max-parallel: 2`. These are per-run
limits, not a reservation of organization-wide runner slots. Shared dependency
changes retain all Python test suites; the controller owns the path decisions.
The TypeScript build is compiled once and its artifact is reused by integration
and smoke jobs, including manual controller runs. A standalone integration
dispatch builds once and shares that artifact with its smoke job. The production
npm audit runs once at the stricter moderate level.
Build and provenance artifacts allow replacement on a same-run retry.

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
this configuration. The npm runtime-pin updater is weekly. Hosted duplicate triage,
upstream docs deployment and hosted evaluation workflows have been removed.
Version-bump jobs targeting external automation/app/enterprise/cloud repositories
have been removed; the local client bump remains an explicit main-branch dispatch.
Example coverage reads the local catalog and checks all examples on both PRs and
main. Catalog edits select the example validation scope.

## Repository settings required for enforcement

The repository currently has no main protection or ruleset. Configure an active
ruleset for `main` in Settings > Rules > Rulesets:

- Require a pull request and at least one approving review.
- Require code-owner review, dismiss approvals after new commits, and require
  approval of the most recent reviewable push.
- Require `SDK CI`, `unresolved-review-threads` and `Validate PR description`
  checks, with GitHub Actions as the expected source.
- Require branches to be up to date.
- Require conversation resolution; block force pushes and branch deletion.
- Keep the bypass list empty unless an explicitly managed emergency process is needed.

`CODEOWNERS` assigns CI and dependency governance to `@Emilio-01-T`. It only
enforces approval when the ruleset requires code-owner review. Preserve the
read-only default Actions token and do not send write tokens/secrets to fork PRs.
Publisher environments may additionally require a human reviewer and main-only
deployment branches. Repository-admin settings cannot be installed through the
current connector and must be set in GitHub.

Do not enable merge queue with the three-check ruleset above yet. The source
controller handles `merge_group`, but the description and review-thread
workflows only report PR checks. Those required metadata checks need separate
merge-group support before that ruleset can use a queue.

The Dependabot file groups security updates but does not enable the repository's
Dependabot alerts/security-update services. Confirm both are enabled under
Settings > Advanced Security. Their status is not exposed to this connector.

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

The Node policy tests cover real Git diffs for docs, client, example, dependency,
workflow, push, manual and merge-group events; artifact identity; missing PR
associations; direct pushes and newer unsuccessful runs. Cross tests in
`tests/cross/test_ci_governance.py` execute the real gate against failures,
cancellations, unexpected skips and missing outputs, and inspect workflow
triggers, build reuse, publication isolation and Dependabot grouping.
Actual Python, binary, Docker and client checks run on GitHub; local
configuration tests do not replace them.
