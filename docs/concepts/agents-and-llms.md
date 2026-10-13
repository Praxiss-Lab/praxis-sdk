# Agents and LLMs

## LLM

`LLM` describes a model, its credential and its transport. Model identifiers follow
the LiteLLM `provider/model` convention, so any supported provider works.

```python
import os
from pydantic import SecretStr
from praxis.sdk import LLM

llm = LLM(
    usage_id="agent",                       # label used in metrics and registries
    model="anthropic/claude-sonnet-5-5",
    api_key=SecretStr(os.environ["LLM_API_KEY"]),
    base_url=os.getenv("LLM_BASE_URL"),     # optional self-hosted endpoint
)
```

Related capabilities, each with a runnable example in the [catalog](../examples/catalog.md):

- **Registry and routing**: several LLMs per conversation, chosen per task.
- **Fallback**: switch to a secondary model when the primary fails.
- **Streaming and reasoning**: token streaming, extended thinking and Responses API reasoning.
- **Metrics**: token usage and cost accounting per `usage_id`.

## Agent

`Agent` combines an LLM with tool specifications and an optional `AgentContext`:

```python
from praxis.sdk import Agent, AgentContext, Tool
from praxis.tools.terminal import TerminalTool

agent = Agent(
    llm=llm,
    tools=[Tool(name=TerminalTool.name)],
    agent_context=AgentContext(system_message_suffix="Answer concisely."),
)
```

For a ready-made configuration with the standard tool set use the preset:

```python
from praxis.tools.preset.default import get_default_agent

agent = get_default_agent(llm=llm, cli_mode=True)  # cli_mode disables browser tools
```

## Security

Agents can run with a confirmation policy and a security analyzer that rates each
action before execution. See examples `04_confirmation_mode_example.py`,
`16_llm_security_analyzer.py`, `32_configurable_security_policy.py` and
`47_defense_in_depth_security.py`.
