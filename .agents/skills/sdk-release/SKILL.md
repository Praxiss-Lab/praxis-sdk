---
name: sdk-release
description: Prepare and verify explicitly authorized Praxis SDK releases using owned repositories, immutable tags and registry credentials.
---

# Praxis SDK release

Ordinary source PRs do not publish a release. While the owner is restructuring
the code and requests source-only verification, merge and validate source
changes without invoking publishers.

For an explicitly requested future release:

1. Verify the exact SDK main commit and required checks. Confirm the planned
   version is new and all Python distributions and the TypeScript client match.
2. Use `prepare-release.yml` in `Praxiss-Lab/praxis-sdk`. Review its release PR
   and generated Agent Server contract before merging.
3. `create-release.yml` handles recognized release PRs and dispatches the owned
   publishers against their immutable tag. This is a publication operation.
4. Verify Python packages, TypeScript packages, container variants and binaries
   independently. The canonical image is
   `ghcr.io/praxiss-lab/praxis-agent-server`.
5. Configure `PRAXIS_PYPI_TOKEN` only when PyPI publication is needed; npm and
   GitHub Packages use their separately configured owned credentials.
6. Use [the post-release checklist](references/post-release-checklist.md).

The detailed workflow map is in
[README-RELEASE](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/.github/workflows/README-RELEASE.md).
No upstream evaluation, Cloud deployment or cross-organization version bump
is part of this release process. Update Praxis's source/image/client pins in a
separate verified application PR when the release is ready for consumption.
