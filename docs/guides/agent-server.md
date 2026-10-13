# Agent Server

The Agent Server hosts conversations, workspaces, terminals, files and settings behind
a REST and WebSocket API. Praxis uses it as its backend; your applications can too,
through `RemoteConversation` or the [TypeScript client](../reference/typescript-client.md).

## Run it

```sh
uv run praxis-agent-server --port 8000
```

| Option                  | Description                                                     |
| ----------------------- | --------------------------------------------------------------- |
| `--host`                | Bind address. Defaults to `127.0.0.1` without a session API key, `0.0.0.0` with one |
| `--port`                | Port, default `8000`                                            |
| `--import-modules`      | Comma-separated modules to import at startup (custom tools)    |
| `--extra-python-path`   | Extra directories on `sys.path` for custom tool imports        |
| `--check-browser`       | Check browser support and exit                                  |

The `agent-server` executable is an equivalent historical name.

## Authentication

Set `SESSION_API_KEY` (or `OH_SESSION_API_KEYS_0`) before exposing the server beyond
loopback. Clients send the key with every request. Put the server behind TLS when it is
reachable over a network.

## Connect from Python

```python
from praxis.sdk import Conversation, Workspace

workspace = Workspace(host="http://127.0.0.1:8000", working_dir="/tmp/work")
conversation = Conversation(agent=agent, workspace=workspace)
conversation.send_message("Hello from a remote client")
conversation.run()
```

## Containers

`DockerWorkspace` starts the server inside a container automatically. Apptainer and
Agent Sandbox (Kubernetes) variants are in [`examples/02_remote_agent_server`](https://github.com/Praxiss-Lab/praxis-sdk/tree/main/examples/02_remote_agent_server).
For a persistent server on your own VM, see the
[Praxis self-hosting guide](https://github.com/Praxiss-Lab/praxis/blob/documentation/docs/SELF_HOSTING.md).
