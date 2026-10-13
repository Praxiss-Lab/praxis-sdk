# Praxis SDK

Python and TypeScript building blocks for agents, tools, conversations and personal
Agent Servers. Maintained by [Praxiss-Lab](https://github.com/Praxiss-Lab).

## Install from the owned repository

```sh
git clone https://github.com/Praxiss-Lab/praxis-sdk.git
cd praxis-sdk
uv sync --frozen --group dev
```

Read [independent deployment](https://praxiss-lab.github.io/praxis-sdk/independent-deployment/) before configuring
models, remote servers or optional critic services. Select your own model provider
and credentials; hosted OpenHands Cloud endpoints are unsupported.

## Examples and documentation

- [Documentation site](https://praxiss-lab.github.io/praxis-sdk/)
- [Example catalog](https://praxiss-lab.github.io/praxis-sdk/examples/catalog/)
- [CI policy](https://praxiss-lab.github.io/praxis-sdk/ci-policy/)
- [TypeScript client](clients/typescript/)
- [Source and issues](https://github.com/Praxiss-Lab/praxis-sdk)

Praxis consumes this SDK for native and container deployments. Automation lives
in the Praxis repository. Use `from praxis.sdk import Agent, Conversation, LLM` for the public namespace.
Historical `openhands.*` imports and serialized identifiers remain compatible
and share the same implementation objects.

## Attribution

This project derives from the OpenHands Software Agent SDK. Copyright and license
notices are preserved in [LICENSE](LICENSE); this attribution does not imply an
upstream hosted-service dependency or affiliation.
