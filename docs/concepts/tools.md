# Tools

Tools are typed actions the agent can call. Each tool defines an action schema, an
observation schema and an executor. Agents reference tools by name with `Tool(name=...)`;
the executor is resolved from the registry when the conversation starts.

## Built-in tools

| Module                              | Purpose                                         |
| ----------------------------------- | ----------------------------------------------- |
| `praxis.tools.terminal`             | Persistent shell sessions                       |
| `praxis.tools.file_editor`          | View, create and edit files                     |
| `praxis.tools.apply_patch`          | Apply unified patches                           |
| `praxis.tools.glob`, `.grep`        | Search files and contents                       |
| `praxis.tools.task_tracker`         | Structured task lists                           |
| `praxis.tools.planning_file_editor` | Planning-mode editing                           |
| `praxis.tools.browser_use`          | Browser automation                              |
| `praxis.tools.delegate`, `.task`    | Sub-agents and task delegation                  |

Presets in `praxis.tools.preset` assemble common sets (`default`, `planning`, `gpt5`, `gemini`).

## Custom tools

Subclass `ToolDefinition`, implement an executor and register it with `register_tool`.
See [`02_custom_tools.py`](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/02_custom_tools.py) and, for
remote servers, [`06_custom_tool`](https://github.com/Praxiss-Lab/praxis-sdk/tree/main/examples/02_remote_agent_server/06_custom_tool).

## MCP

Model Context Protocol servers can be attached to an agent so their tools appear next
to built-in ones, including OAuth-protected servers. See `07_mcp_integration.py` and
`08_mcp_with_oauth.py`. MCP servers are operator-owned: review what they can access.
