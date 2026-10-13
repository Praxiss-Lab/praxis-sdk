# Praxis SDK post-release checklist

Use this only after an authorized release has actually been published.

- Verify the GitHub tag and release match the reviewed commit.
- Check every publisher's exact version, checksums and immutable source.
- Verify the owned GHCR manifest and native container health for the supported
  architectures. Verify downloadable server binaries independently.
- Verify Python distribution and TypeScript package names belong to Praxis.
- Test the owned example catalog and relevant integrations on operator-managed
  infrastructure with explicitly configured model endpoints.
- Update Praxis source, versions and client/image pins in a reviewed PR.
- Document incomplete publication rather than implying that source merges
  automatically replace existing release archives or container images.

No hosted evaluation CDN, upstream workflow dispatch or Cloud staging account
is required. Registry cleanup is separate from source integration; inventory
owned packages and remaining consumers before deleting an old artifact.
