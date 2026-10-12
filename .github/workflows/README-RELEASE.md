# Praxis SDK release workflows

Source integration and artifact publication are separate. Ordinary PR merges
run source validation and can reuse successful exact-tree PR evidence. They
do not publish new packages, images or releases. Existing published artifacts
retain their previous contents until an explicitly authorized new release.

## Future authorized publication

1. Verify main, choose a new `X.Y.Z` version, and run `prepare-release.yml`.
   Review synchronized Python/TypeScript versions and generated API contracts.
2. Merge only that validated release PR. `create-release.yml` recognizes its
   release markers, creates the immutable tag/release and explicitly dispatches
   the publishers. This step publishes artifacts.
3. Verify each publisher independently and record its exact commit and version.

| Workflow | Purpose |
| --- | --- |
| `pypi-release.yml` | Publish `praxis-sdk`, `praxis-tools`, `praxis-workspace` and `praxis-agent-server` with `PRAXIS_PYPI_TOKEN`. |
| `typescript-client-npm-publish.yml` | Publish the owned `@praxiss-lab/praxis-sdk-client` npm package. |
| `typescript-client-github-packages-publish.yml` | Publish the owned TypeScript client to GitHub Packages. |
| `server.yml` | Manually publish versioned `ghcr.io/praxiss-lab/praxis-agent-server` images and multi-architecture manifests. |
| `release-binaries.yml` | Manually publish verified server binaries, `openapi.json` and checksums for an existing release tag. |
| `version-bump-prs.yml` | Maintain the TypeScript client in this repository; no upstream application or automation PR is dispatched. |

Publishers are dispatch-only and use immutable release tags. They do not
listen for every PR, main push or release event. PR server validation can
build temporary binaries/container artifacts for tests without publishing.

## Prerequisites and recovery

Registry credentials and package permissions must belong to the operator's
accounts. Configure publication credentials only when publication is requested;
none is needed to integrate the current source rebranding. Never reuse an
upstream registry credential or dispatch an upstream Cloud/evaluation job.

Retry a failed publisher at the same immutable release tag after diagnosing
the failed step. Verify image variants, architecture coverage, API version and
checksums before updating Praxis consumption pins. There is no automatic
upstream automation release or Cloud deployment in this process.

Delete obsolete registry artifacts only after inventorying owned packages,
versions and consumers. Deleting a package does not alter Git history or the
contents of existing release archives and container images.
