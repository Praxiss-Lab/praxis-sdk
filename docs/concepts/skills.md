# Skills

Skills are reusable instructions, optionally with scripts and reference files, that
are injected into the agent's context. A skill is always active or activated by a
trigger.

| Trigger          | Activates when                                        |
| ---------------- | ----------------------------------------------------- |
| none             | Always (repository guidance such as `AGENTS.md`)      |
| `KeywordTrigger` | A user message contains one of the keywords          |
| `TaskTrigger`    | A task matches the skill                             |
| `PathTrigger`    | The agent works on matching file paths               |

## Where skills are loaded from

- **Repository**: `AGENTS.md` at the repository root and skills under `.agents/skills/`.
- **User**: `~/.openhands/skills/` (historical directory name kept for compatibility).
- **Installed**: skills installed with `install_skill`, stored under `~/.openhands/skills/installed/`.

## Repository memory with `AGENTS.md`

Put repository-specific knowledge in `AGENTS.md`: build commands, conventions,
architecture notes. It is loaded into every conversation, and agents can update it to
keep useful knowledge across sessions.

## Inline skills

```python
from praxis.sdk import AgentContext
from praxis.sdk.context import KeywordTrigger, Skill

context = AgentContext(
    skills=[
        Skill(
            name="release-notes",
            content="When writing release notes, group changes by user impact.",
            trigger=KeywordTrigger(keywords=["release notes"]),
        )
    ]
)
```

See [`03_activate_skill.py`](../../examples/01_standalone_sdk/03_activate_skill.py) for a complete example.
