---
name: feature-release-rollout
description: Coordinate a source feature across Praxis SDK, Praxis, owned documentation and optional explicitly authorized releases.
---

# Praxis feature rollout

Map the change to the SDK implementation, Python/TypeScript contracts, Praxis
backend/controller, frontend, automation and documentation. Use only the owned
`Praxiss-Lab/praxis-sdk` and `Praxiss-Lab/Praxis` repositories. No separate
upstream CLI, enterprise deployment, marketing or documentation service is
required.

Record the SDK commit in Praxis configuration and keep version, source and
vendored-client mirrors consistent. Test affected layers and cross-repository
contracts before integrating the source changes. Document any migration of
settings or persisted state and preserve historical identifiers when needed.

Update each repository's README, examples and operational guides alongside the
feature. Report whether source integration is complete separately from whether
artifacts have been published. During structural work, source integration and
verification can proceed without any new package, image or release.

If publication is explicitly requested later, follow the owned SDK release
guide and the Praxis release workflow. Publish immutable verified versions;
do not dispatch jobs to upstream repositories or hosted Cloud services.
