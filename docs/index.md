---
hide:
  - navigation
  - toc
---

<div class="praxis-hero" markdown>

![Praxis](assets/brand/praxis-primary.png#only-light)
![Praxis](assets/brand/praxis-primary-white.png#only-dark)

# Praxis SDK

Python and TypeScript building blocks for agents, tools, conversations and
personal Agent Servers. Maintained by [Praxiss-Lab](https://github.com/Praxiss-Lab).

[Get started](getting-started/installation.md){ .md-button .md-button--primary }
[Example catalog](examples/catalog.md){ .md-button }

</div>

<div class="grid cards" markdown>

-   :material-robot-outline: **Agents and LLMs**

    ---

    Combine any model provider with tools, skills and security policies.

    [:octicons-arrow-right-24: Agents and LLMs](concepts/agents-and-llms.md)

-   :material-message-text-outline: **Conversations**

    ---

    Run, pause, persist and fork agent conversations locally or remotely.

    [:octicons-arrow-right-24: Conversations](concepts/conversations.md)

-   :material-server-outline: **Personal Agent Servers**

    ---

    Host agents on your own machine, VM or container. Your VM is your personal cloud.

    [:octicons-arrow-right-24: Agent Server](guides/agent-server.md)

-   :material-shield-check-outline: **Independent by design**

    ---

    No hosted account required: you choose the model provider, credentials and infrastructure.

    [:octicons-arrow-right-24: Independent deployment](independent-deployment.md)

</div>

## Packages

| Package               | Namespace              | Purpose                                                     |
| --------------------- | ---------------------- | ----------------------------------------------------------- |
| `praxis-sdk`          | `praxis.sdk`           | Agents, LLMs, conversations, events, skills, hooks          |
| `praxis-tools`        | `praxis.tools`         | Terminal, file editor, browser, task tracker, delegation... |
| `praxis-workspace`    | `praxis.workspace`     | Docker, Apptainer and remote API workspaces                 |
| `praxis-agent-server` | `praxis.agent_server`  | REST and WebSocket server hosting conversations             |

Praxis, the agent workspace application, consumes this SDK for native and container
deployments: see the [Praxis documentation](https://praxiss-lab.github.io/praxis/).

!!! note "Attribution"
    This project derives from the OpenHands Software Agent SDK. Copyright and license
    notices are preserved in [LICENSE](../LICENSE); this attribution does not imply an
    upstream hosted-service dependency or affiliation.
