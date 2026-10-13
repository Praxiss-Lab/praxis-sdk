# Compatibility identifiers

Praxis SDK derives from the OpenHands Software Agent SDK. Some technical names are
kept so that existing code and data keep working. They are labels, not connections
to upstream services: all of them resolve to this repository's implementation.

| Kind                     | Examples                                         | Why it is kept                                         |
| ------------------------ | ------------------------------------------------ | ------------------------------------------------------ |
| Python imports           | `openhands.sdk`, `openhands.tools`               | Same module objects as `praxis.sdk`, `praxis.tools`    |
| Serialized identifiers   | class names and `openhands` values in saved data | Old conversations and settings stay readable           |
| Environment variables    | `OH_SESSION_API_KEYS_0`, `OH_AGENT_SERVER_GIT_REF` | Existing deployments keep their configuration         |
| Data directories         | `~/.openhands/...`                               | Existing conversations, settings and skills are found |
| Executables              | `agent-server`                                   | Scripts that call the old name keep working           |

New code should use the `praxis.*` namespace and `praxis-agent-server`. Removing the
historical identifiers requires a coordinated migration of code, configuration and
stored data; it is planned as a separate change.
