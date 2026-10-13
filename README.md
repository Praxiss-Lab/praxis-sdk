# Praxis SDK documentation

This `documentation` branch holds only the documentation site, published at
<https://praxiss-lab.github.io/praxis-sdk/>. It is independent of `main`: changes here
never run the application CI.

## Edit and preview

```sh
pip install 'mkdocs>=1.6,<2' 'mkdocs-material>=9.6,<10'
mkdocs serve
```

Pages live in `docs/` and the navigation in `mkdocs.yml`. Open pull requests
against `documentation`; the Documentation workflow builds them strictly and deploys to
GitHub Pages after merge. Links to repository files outside `docs/` point to `main`.
