<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/brand/praxis-primary-white.png">
    <img src="docs/assets/brand/praxis-primary.png" alt="Praxis" width="420">
  </picture>
</p>

# Praxis SDK documentation

Python and TypeScript building blocks for agents, tools, conversations and personal
Agent Servers. Maintained by [Praxiss-Lab](https://github.com/Praxiss-Lab).

This `documentation` branch is the only home of the Praxis SDK documentation. It is
independent of `main`: edit the Markdown files here through pull requests into
`documentation`; changes never run SDK CI. Source code lives on
[`main`](https://github.com/Praxiss-Lab/praxis-sdk).

## Get started

- [Installation](docs/getting-started/installation.md)
- [Your first agent](docs/getting-started/first-agent.md)

## Concepts

- [Architecture](docs/concepts/architecture.md): packages, namespaces and the event model.
- [Agents and LLMs](docs/concepts/agents-and-llms.md)
- [Conversations](docs/concepts/conversations.md)
- [Tools](docs/concepts/tools.md)
- [Workspaces](docs/concepts/workspaces.md)
- [Skills](docs/concepts/skills.md)

## Guides

- [Agent Server](docs/guides/agent-server.md): host conversations on your own machine, VM or container.
- [Local LLMs](docs/guides/local-llms.md): Ollama, LM Studio, vLLM and context windows.
- [Independent deployment](docs/independent-deployment.md): no hosted account required.
- [Example catalog](docs/examples/catalog.md): every runnable example and how to run it.

## Reference

- [TypeScript client](docs/reference/typescript-client.md)
- [Compatibility identifiers](docs/reference/compatibility.md)
- [CI policy](docs/ci-policy.md)

## Packages

| Package               | Namespace             | Purpose                                                     |
| --------------------- | --------------------- | ----------------------------------------------------------- |
| `praxis-sdk`          | `praxis.sdk`          | Agents, LLMs, conversations, events, skills, hooks          |
| `praxis-tools`        | `praxis.tools`        | Terminal, file editor, browser, task tracker, delegation... |
| `praxis-workspace`    | `praxis.workspace`    | Docker, Apptainer and remote API workspaces                 |
| `praxis-agent-server` | `praxis.agent_server` | REST and WebSocket server hosting conversations             |

Praxis, the agent workspace application, consumes this SDK: see the
[Praxis documentation](https://github.com/Praxiss-Lab/praxis/tree/documentation).

This project derives from the OpenHands Software Agent SDK. Copyright and license
notices are preserved in [LICENSE](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/LICENSE);
this attribution does not imply an upstream hosted-service dependency or affiliation.
