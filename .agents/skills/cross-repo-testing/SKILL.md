---
name: cross-repo-testing
description: Verify contracts between the owned Praxis SDK and Praxis application using immutable source pins and operator-managed backends.
---

# Praxis cross-repository verification

The repositories are [praxis-sdk](https://github.com/Praxiss-Lab/praxis-sdk)
and [Praxis](https://github.com/Praxiss-Lab/Praxis). Automation is maintained
under `vendor/automation` in Praxis. No upstream deployment repository or hosted
staging environment is part of this verification.

1. Record both commit SHAs. Inspect `config/defaults.json` in Praxis for its
   immutable SDK source pin, package versions, ports and backend configuration.
2. Run the relevant SDK tests, compatibility checks and TypeScript tests.
   Run the affected Praxis tests and type checks. Keep Python serialized
   identities, settings and API contracts compatible.
3. Test the native backend on loopback. Verify `/health`, `/server_info` and
   settings before conversation, workspace and automation behavior.
4. When container validation is available, build from the same source commits
   and verify native, complete-container and separate frontend/backend modes.
5. A remote backend must be an operator-owned endpoint explicitly configured
   for the test. Supply credentials through the approved secret mechanism.
   Never infer a hosted endpoint from a model ID or historical workspace class.

An application PR may pin a verified SDK commit before publication. Report the
exact commits, executed checks and unavailable runtime environments. Merging a
source change does not require publishing new images or registry packages.
