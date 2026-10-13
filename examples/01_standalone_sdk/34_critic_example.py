"""Iterative Refinement with Critic Model Example.

This is EXPERIMENTAL.

This example demonstrates how to use a critic model to shepherd an agent through
complex, multi-step tasks. The critic evaluates the agent's progress and provides
feedback that can trigger follow-up prompts when the agent hasn't completed the
task successfully.

Key concepts demonstrated:
1. Setting up a critic with IterativeRefinementConfig for automatic retry
2. Conversation.run() automatically handling critic-driven refinement
3. Customizing refinement policy independently of variable critic scores
4. Bounding agent work and verifying the final artifact

Configure CRITIC_BASE_URL and CRITIC_API_KEY for an optional self-hosted critic
using the same base_url with /vllm suffix and "critic" as the model name.
"""

import os
import tempfile
from pathlib import Path

from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.sdk.agent.critic_mixin import ITERATIVE_REFINEMENT_ITERATION_KEY
from openhands.sdk.conversation.state import ConversationExecutionStatus
from openhands.sdk.critic import APIBasedCritic, CriticResult, IterativeRefinementConfig
from openhands.sdk.critic.base import CriticBase
from openhands.tools.file_editor import FileEditorTool


# Keep the live example deterministic and comfortably inside the harness timeout:
# one initial attempt, one critic-driven refinement, and bounded agent steps.
MAX_REFINEMENTS = 1
MAX_AGENT_STEPS = 10


class SingleRefinementCritic(APIBasedCritic):
    """Always demonstrate exactly one refinement, regardless of score variance."""

    def should_refine(self, critic_result: CriticResult) -> bool:  # noqa: ARG002
        return True


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    raise ValueError(
        f"Missing required environment variable: {name}. "
        f"Set {name} before running this example."
    )


def get_default_critic() -> CriticBase | None:
    """Configure an optional operator-managed critic service."""
    server_url = os.environ.get("CRITIC_BASE_URL")
    api_key = os.environ.get("CRITIC_API_KEY")
    if not server_url or not api_key:
        return None
    return SingleRefinementCritic(
        server_url=server_url,
        api_key=api_key,
        model_name=os.environ.get("CRITIC_MODEL", "critic"),
    )


INITIAL_TASK_PROMPT = """\
Create `greeting.txt` containing exactly this one line, including the final newline:

Hello from the Praxis critic example!

Use the file editor, verify the content once, then finish. Do not create other files,
initialize version control, or perform unrelated work.
"""

EXPECTED_GREETING = "Hello from the Praxis critic example!\n"


llm_api_key = get_required_env("LLM_API_KEY")
llm_model = os.getenv("LLM_MODEL", "anthropic/claude-haiku-4-5-20251001")
llm = LLM(
    model=llm_model,
    api_key=llm_api_key,
    temperature=0,
    base_url=os.getenv("LLM_BASE_URL"),
)

# The critic always requests one refinement, making this behavior independent of
# model score variance while still exercising the real critic API.
iterative_config = IterativeRefinementConfig(max_iterations=MAX_REFINEMENTS)

# Configure critic from operator-managed endpoint or explicit env vars
critic = get_default_critic()
if critic is None:
    print(
        "⚠️  No operator-managed critic endpoint configured, trying explicit env vars..."
    )
    critic = SingleRefinementCritic(
        server_url=get_required_env("CRITIC_SERVER_URL"),
        api_key=get_required_env("CRITIC_API_KEY"),
        model_name=get_required_env("CRITIC_MODEL_NAME"),
        iterative_refinement=iterative_config,
    )
else:
    # Add iterative refinement config to the auto-configured critic
    critic = critic.model_copy(update={"iterative_refinement": iterative_config})

# Create agent with critic (iterative refinement is built into the critic)
agent = Agent(
    llm=llm,
    tools=[Tool(name=FileEditorTool.name)],
    critic=critic,
)

# Create workspace
workspace = Path(tempfile.mkdtemp(prefix="critic_demo_"))
print(f"📁 Created workspace: {workspace}")

# Create conversation - iterative refinement is handled automatically
# by Conversation.run() based on the critic's config
conversation = Conversation(
    agent=agent,
    workspace=str(workspace),
    max_iteration_per_run=MAX_AGENT_STEPS,
)

print("\n" + "=" * 70)
print("🚀 Starting Iterative Refinement with Critic Model")
print("=" * 70)
print(f"Refinements: {MAX_REFINEMENTS}")
print(f"Max agent steps: {MAX_AGENT_STEPS}")

conversation.send_message(INITIAL_TASK_PROMPT)
conversation.run()

if conversation.state.execution_status is not ConversationExecutionStatus.FINISHED:
    raise RuntimeError(
        f"Conversation ended with {conversation.state.execution_status.value}"
    )
if workspace.joinpath("greeting.txt").read_text() != EXPECTED_GREETING:
    raise RuntimeError("greeting.txt does not contain the expected text")
refinement_count = conversation.state.agent_state.get(
    ITERATIVE_REFINEMENT_ITERATION_KEY, 0
)
if refinement_count != MAX_REFINEMENTS:
    raise RuntimeError(
        f"Expected {MAX_REFINEMENTS} refinement, observed {refinement_count}"
    )

print(f"Completed {refinement_count} critic-driven refinement.")
print("Verified greeting.txt.")

# Report cost
cost = llm.metrics.accumulated_cost
print(f"\nEXAMPLE_COST: {cost:.4f}")
