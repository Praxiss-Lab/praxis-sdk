---
name: debug-test-examples-workflow
description: Diagnose the owned example catalog and explicitly requested live example runs without bypassing source validation.
---

# Praxis example checks

`check-documented-examples.yml` validates the owned catalog during SDK
Validation. The catalog is `docs/examples/catalog.md`; examples remain under
`examples/` in this repository.

Inspect the failing job in `Praxiss-Lab/praxis-sdk`, reproduce its command at
the exact head commit and correct the catalog, example or contract. Do not
remove a failing example or weaken validation merely to make the gate green.

`run-examples.yml` is a manual workflow on the default branch. Run it only when
live examples have been explicitly requested and the operator has configured
the model, base URL, credentials and owned backend prerequisites. Adding or
toggling a PR label does not dispatch this workflow.

For logs, use the repository's Actions run and failed job. Keep tokens out of
command output and reports. Report unit/catalog validation separately from
live provider or container tests that were actually executed.
