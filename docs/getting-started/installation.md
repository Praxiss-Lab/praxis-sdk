# Installation

Praxis SDK is installed from the owned repository. It requires Python 3.12 or later
and [`uv`](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/Praxiss-Lab/praxis-sdk.git
cd praxis-sdk
uv sync --frozen --group dev
```

The workspace installs four packages together: `praxis-sdk`, `praxis-tools`,
`praxis-workspace` and `praxis-agent-server`. See [Architecture](../concepts/architecture.md)
for what each one provides.

## Configure a model

Praxis SDK does not ship with a default hosted model. Choose your provider and export
its credential:

```sh
export LLM_MODEL="anthropic/claude-sonnet-5-5"   # any LiteLLM-compatible model id
export LLM_API_KEY="..."                          # your provider key
export LLM_BASE_URL="..."                         # optional: self-hosted proxy or local server
```

For Ollama, LM Studio, vLLM and other local servers see [Local LLMs](../guides/local-llms.md).
Read [Independent deployment](../independent-deployment.md) before configuring
remote servers or optional critic services.

## Verify the installation

```sh
uv run python -c "from praxis.sdk import Agent, Conversation, LLM; print('Praxis SDK ready')"
```

Next: [build your first agent](first-agent.md).
