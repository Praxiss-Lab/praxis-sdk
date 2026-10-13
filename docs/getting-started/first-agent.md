# Your first agent

This example creates an agent with a terminal, a file editor and a task tracker, then
asks it to work in the current directory. It mirrors
[`examples/01_standalone_sdk/01_hello_world.py`](../../examples/01_standalone_sdk/01_hello_world.py).

```python
import os

from praxis.sdk import LLM, Agent, Conversation, Tool
from praxis.tools.file_editor import FileEditorTool
from praxis.tools.task_tracker import TaskTrackerTool
from praxis.tools.terminal import TerminalTool

llm = LLM(
    model=os.environ["LLM_MODEL"],
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)

agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
        Tool(name=TaskTrackerTool.name),
    ],
)

conversation = Conversation(agent=agent, workspace=os.getcwd())
conversation.send_message("Write 3 facts about the current project into FACTS.txt.")
conversation.run()
```

Run it from the repository root:

```sh
uv run python examples/01_standalone_sdk/01_hello_world.py
```

!!! warning "The agent acts on your machine"
    With a local workspace, terminal and file tools operate directly on the host
    filesystem. Use a dedicated directory, or a [Docker workspace](../concepts/workspaces.md),
    for untrusted tasks.

## What happened

1. `LLM` describes the model and its credential.
2. `Agent` combines the LLM with tool specifications.
3. `Conversation` binds the agent to a workspace and stores the event history.
4. `run()` loops: the agent reasons, calls tools and observes results until it finishes.

## Next steps

- Learn the building blocks in [Concepts](../concepts/architecture.md).
- Browse more than 70 runnable programs in the [Example catalog](../examples/catalog.md).
- Host conversations remotely with the [Agent Server](../guides/agent-server.md).
