# Conversations

A `Conversation` binds an agent to a workspace and records every event.

```python
from praxis.sdk import Conversation

conversation = Conversation(agent=agent, workspace="/path/to/project")
conversation.send_message("Run the test suite and fix the first failure.")
conversation.run()
```

`Conversation(...)` returns a local conversation for a path or `LocalWorkspace`, and a
`RemoteConversation` when the workspace points to an [Agent Server](../guides/agent-server.md).

## Lifecycle

| Operation                     | Use                                                          |
| ----------------------------- | ------------------------------------------------------------ |
| `send_message(...)`           | Add a user message; it can be sent while the agent is running |
| `run()`                       | Execute until the agent finishes, pauses or needs confirmation |
| `pause()`                     | Stop after the current step                                   |
| `persistence_dir=...`         | Store events on disk and resume by `conversation_id`         |
| fork                          | Branch a conversation to explore alternatives                 |

## Callbacks and visualization

Pass `callbacks=[fn]` to receive every event as it happens, or provide a custom
visualizer. The `11_async.py` and `50_async_cancellation.py` examples show asynchronous use.

## Context management

Long conversations are compacted by a **condenser** that summarizes older events,
and a **stuck detector** stops loops that repeat without progress. See
`14_context_condenser.py` and `20_stuck_detector.py`.
