# Workspaces

A workspace is where tools execute: commands, files and processes.

| Workspace            | Package             | Runs on                                              |
| -------------------- | ------------------- | ---------------------------------------------------- |
| `LocalWorkspace`     | `praxis.sdk`        | The current host (a plain path is accepted too)      |
| `RemoteWorkspace`    | `praxis.sdk`        | An existing [Agent Server](../guides/agent-server.md) |
| `DockerWorkspace`    | `praxis.workspace`  | A container started from an Agent Server image       |
| Apptainer            | `praxis.workspace`  | An Apptainer/Singularity container                   |
| Agent Sandbox        | `praxis.workspace`  | A Kubernetes Agent Sandbox deployment                |

## Docker

```python
from praxis.workspace import DockerWorkspace

with DockerWorkspace(server_image=server_image) as workspace:
    conversation = Conversation(agent=agent, workspace=workspace)
    conversation.send_message("Install dependencies and run the tests.")
    conversation.run()
```

The container is stopped when the context manager exits. See
[`02_convo_with_docker_sandboxed_server.py`](../../examples/02_remote_agent_server/02_convo_with_docker_sandboxed_server.py).

## Remote server

```python
from praxis.sdk import Workspace

workspace = Workspace(host="http://my-vm:8000", working_dir="/workspace/project")
```

!!! info "Provisioning APIs"
    The legacy `APIRemoteWorkspace` and cloud workspace classes only work with a
    compatible provisioning service that you operate. Hosted upstream URLs are rejected.
    See [Independent deployment](../independent-deployment.md).
