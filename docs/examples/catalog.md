# Praxis SDK example catalog

This catalog describes repository examples, entry points and supporting modules.
The commands below apply to executable scripts; helper modules are imported by
their accompanying entry point. Read the source before choosing a command.
Read [independent deployment](../independent-deployment.md) before running them.
Model-backed examples require an operator-selected model and credential; remote
examples require a compatible personal server. Source-specific arguments and
prerequisites remain in each linked script. Provisioning samples with legacy API
names require an operator-managed compatible App API; upstream hosted services
are disabled. Listing an example is not evidence of a live model or Docker run.

## 01 standalone sdk

### 01 hello world

Demonstrates hello world.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/01_hello_world.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/01_hello_world.py`.

### 02 custom tools

Advanced example showing explicit executor usage and custom grep tool.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/02_custom_tools.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/02_custom_tools.py`.

### 03 activate skill

Demonstrates activate skill.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/03_activate_skill.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/03_activate_skill.py`.

### 04 confirmation mode example

Praxis Agent SDK — Confirmation Mode Example

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/04_confirmation_mode_example.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/04_confirmation_mode_example.py`.

### 05 use llm registry

Demonstrates use llm registry.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/05_use_llm_registry.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/05_use_llm_registry.py`.

### 06 interactive terminal w reasoning

Demonstrates interactive terminal w reasoning.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/06_interactive_terminal_w_reasoning.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/06_interactive_terminal_w_reasoning.py`.

### 07 mcp integration

Demonstrates mcp integration.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/07_mcp_integration.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/07_mcp_integration.py`.

### 08 mcp with oauth

Demonstrates mcp with oauth.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/08_mcp_with_oauth.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/08_mcp_with_oauth.py`.

### 09 pause example

Demonstrates pause example.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/09_pause_example.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/09_pause_example.py`.

### 10 persistence

Demonstrates persistence.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/10_persistence.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/10_persistence.py`.

### 11 async

This example demonstrates usage of a Conversation in an async context
(e.g.: From a fastapi server). The conversation is run in a background
thread and a callback with results is executed in the main runloop

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/11_async.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/11_async.py`.

### 12 custom secrets

Demonstrates custom secrets.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/12_custom_secrets.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/12_custom_secrets.py`.

### 13 get llm metrics

Demonstrates get llm metrics.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/13_get_llm_metrics.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/13_get_llm_metrics.py`.

### 14 context condenser

To manage context in long-running conversations, the agent can use a context condenser
that keeps the conversation history within a specified size limit. This example
demonstrates using the `LLMSummarizingCondenser`, which automatically summarizes
older parts of the conversation when the history exceeds a defined threshold.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/14_context_condenser.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/14_context_condenser.py`.

### 15 browser use

Demonstrates browser use.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/15_browser_use.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/15_browser_use.py`.

### 16 llm security analyzer

Praxis Agent SDK — LLM Security Analyzer Example (Simplified)

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/16_llm_security_analyzer.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/16_llm_security_analyzer.py`.

### 17 image input

Praxis Agent SDK — Image Input Example.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/17_image_input.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/17_image_input.py`.

### 18 send message while processing

Example demonstrating that user messages can be sent and processed while
an agent is busy.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/18_send_message_while_processing.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/18_send_message_while_processing.py`.

### 19 llm routing

Demonstrates llm routing.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/19_llm_routing.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/19_llm_routing.py`.

### 20 stuck detector

Demonstrates stuck detector.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/20_stuck_detector.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/20_stuck_detector.py`.

### 21 generate extraneous conversation costs

Demonstrates generate extraneous conversation costs.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/21_generate_extraneous_conversation_costs.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/21_generate_extraneous_conversation_costs.py`.

### 22 anthropic thinking

Example demonstrating Anthropic's extended thinking feature with thinking blocks.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/22_anthropic_thinking.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/22_anthropic_thinking.py`.

### 23 responses reasoning

Example: Responses API path via LiteLLM in a Real Agent Conversation

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/23_responses_reasoning.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/23_responses_reasoning.py`.

### 24 planning agent workflow

Planning Agent Workflow Example

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/24_planning_agent_workflow.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/24_planning_agent_workflow.py`.

### 25 agent delegation

Agent Delegation Example

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/25_agent_delegation.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/25_agent_delegation.py`.

### 26 custom visualizer

Custom Visualizer Example

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/26_custom_visualizer.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/26_custom_visualizer.py`.

### 27 observability laminar

Observability & Laminar example

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/27_observability_laminar.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/27_observability_laminar.py`.

### 28 ask agent example

Example demonstrating the ask_agent functionality for getting sidebar replies
from the agent for a running conversation.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/28_ask_agent_example.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/28_ask_agent_example.py`.

### 29 llm streaming

Demonstrates llm streaming.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/29_llm_streaming.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/29_llm_streaming.py`.

### 30 tom agent

Example demonstrating Tom agent with Theory of Mind capabilities.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/30_tom_agent.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/30_tom_agent.py`.

### 31 iterative refinement

Iterative Refinement Example: COBOL to Java Refactoring

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/31_iterative_refinement.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/31_iterative_refinement.py`.

### 32 configurable security policy

Praxis Agent SDK — Configurable Security Policy Example

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/32_configurable_security_policy.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/32_configurable_security_policy.py`.

### main

Praxis Agent SDK — Hooks Example

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/33_hooks/main.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/33_hooks/main.py`.

### 34 critic example

Iterative Refinement with Critic Model Example.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/34_critic_example.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/34_critic_example.py`.

### 35 subscription login

Example: Using ChatGPT subscription for Codex models.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/35_subscription_login.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/35_subscription_login.py`.

### 36 event json to openai messages

Load persisted events and convert them into LLM-ready messages.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/36_event_json_to_openai_messages.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/36_event_json_to_openai_messages.py`.

### main

Example: Using LLMProfileStore to save and reuse LLM configurations.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/37_llm_profile_store/main.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/37_llm_profile_store/main.py`.

### 38 browser session recording

Browser Session Recording Example

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/38_browser_session_recording.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/38_browser_session_recording.py`.

### 39 llm fallback

Example: Using FallbackStrategy for LLM resilience.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/39_llm_fallback.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/39_llm_fallback.py`.

### 40 acp agent example

Example: Using ACPAgent with Claude Code ACP server.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/40_acp_agent_example.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/40_acp_agent_example.py`.

### 41 task tool set

Animal Quiz with Task Tool Set

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/41_task_tool_set.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/41_task_tool_set.py`.

### 42 file based subagents

Example: Defining a sub-agent inline with AgentDefinition.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/42_file_based_subagents.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/42_file_based_subagents.py`.

### 44 model switching in convo

Mid-conversation model switching.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/44_model_switching_in_convo.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/44_model_switching_in_convo.py`.

### 45 parallel tool execution

Example: Parallel tool execution with tool_concurrency_limit.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/45_parallel_tool_execution.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/45_parallel_tool_execution.py`.

### 46 agent settings

Create, serialize, and deserialize PraxisAgentSettings, then build an agent.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/46_agent_settings.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/46_agent_settings.py`.

### 47 defense in depth security

Defense-in-Depth Security: composing local analyzers with ConfirmRisky.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/47_defense_in_depth_security.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/47_defense_in_depth_security.py`.

### 48 conversation fork

Branch a conversation. The conversation is a tree (every event has a
``parent_id``; the HEAD is ``leaf_event_id``), exposing three primitives:

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/48_conversation_fork.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/48_conversation_fork.py`.

### 49 switch llm tool

Switch LLM profiles with the built-in switch_llm tool.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/49_switch_llm_tool.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/49_switch_llm_tool.py`.

### 50 async cancellation

Async interrupt demo — cancel during LLM reasoning *or* tool execution.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/50_async_cancellation.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/50_async_cancellation.py`.

### main

Praxis Agent SDK — Agent-based Hooks Example

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/51_agent_hooks/main.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/51_agent_hooks/main.py`.

### 52 dynamic workflow

Dynamic workflow tool example.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/52_dynamic_workflow.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/52_dynamic_workflow.py`.

### 53 client defined tools

Demonstrate client-defined tools — tools registered via JSON spec that are
executed by an external client (e.g. a browser frontend), not the SDK itself.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/53_client_defined_tools.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/53_client_defined_tools.py`.

### 54 goal completion loop

The /goal command: pursue an objective until a judge LLM confirms it is done.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/54_goal_completion_loop.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/54_goal_completion_loop.py`.

### 55 persistent memory

Opt-in persistent memory across sessions (two-tier ``MEMORY.md``).

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/55_persistent_memory.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/55_persistent_memory.py`.

### 56 structured output

Structured output via ``response_schema``.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/56_structured_output.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/56_structured_output.py`.

### main

Praxis Agent SDK - prompt-based hooks example.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/57_prompt_hooks/main.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/57_prompt_hooks/main.py`.

### main

Consult the Oracle end-to-end with the ask_oracle tool.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/58_ask_oracle_tool/main.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/58_ask_oracle_tool/main.py`.

### 59 route task to model

Route each task to the best LLM with the built-in route_task_to_model tool.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/01_standalone_sdk/59_route_task_to_model.py)

Run from the repository root: `uv run python examples/01_standalone_sdk/59_route_task_to_model.py`.

## 02 remote agent server

### 01 convo with local agent server

Demonstrates convo with local agent server.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/01_convo_with_local_agent_server.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/01_convo_with_local_agent_server.py`.

### 02 convo with docker sandboxed server

Demonstrates convo with docker sandboxed server.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/02_convo_with_docker_sandboxed_server.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/02_convo_with_docker_sandboxed_server.py`.

### 03 browser use with docker sandboxed server

Demonstrates browser use with docker sandboxed server.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/03_browser_use_with_docker_sandboxed_server.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/03_browser_use_with_docker_sandboxed_server.py`.

### 04 convo with api sandboxed server

Example: APIRemoteWorkspace with Dynamic Build.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/04_convo_with_api_sandboxed_server.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/04_convo_with_api_sandboxed_server.py`.

### 05 vscode with docker sandboxed server

Demonstrates vscode with docker sandboxed server.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/05_vscode_with_docker_sandboxed_server.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/05_vscode_with_docker_sandboxed_server.py`.

### log data

Log Data Tool - Example custom tool for logging structured data to JSON.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/06_custom_tool/custom_tools/log_data.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/06_custom_tool/custom_tools/log_data.py`.

### main

Example: Using custom tools with remote agent server.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/06_custom_tool/main.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/06_custom_tool/main.py`.

### 07 convo with cloud workspace

Example: PraxisCloudWorkspace for operator-managed App API API.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/07_convo_with_cloud_workspace.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/07_convo_with_cloud_workspace.py`.

### 08 convo with apptainer sandboxed server

Demonstrates convo with apptainer sandboxed server.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/08_convo_with_apptainer_sandboxed_server.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/08_convo_with_apptainer_sandboxed_server.py`.

### 09 acp agent with remote runtime

Example: ACPAgent with Remote Runtime via API.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/09_acp_agent_with_remote_runtime.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/09_acp_agent_with_remote_runtime.py`.

### 10 cloud workspace share credentials

Example: Inherit SaaS credentials via PraxisCloudWorkspace.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/10_cloud_workspace_share_credentials.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/10_cloud_workspace_share_credentials.py`.

### 11 conversation fork

Fork a conversation through the agent server REST API.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/11_conversation_fork.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/11_conversation_fork.py`.

### 12 settings and secrets api

Example demonstrating the Settings and Secrets API.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/12_settings_and_secrets_api.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/12_settings_and_secrets_api.py`.

### 13 workspace get llm

Example demonstrating workspace.get_llm() for settings-driven conversations.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/13_workspace_get_llm.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/13_workspace_get_llm.py`.

### 14 client defined tools

Client-defined tools via the agent-server API.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/14_client_defined_tools.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/14_client_defined_tools.py`.

### 15 openai compatible gateway

Use the agent-server through an OpenAI-compatible Chat Completions client.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/15_openai_compatible_gateway.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/15_openai_compatible_gateway.py`.

### 16 deferred init

Example demonstrating deferred-init (warm-pool) mode for the agent server.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/16_deferred_init.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/16_deferred_init.py`.

### 17 convo with agent sandbox server

Run a conversation whose agent server lives in a kubernetes-sigs/agent-sandbox pod.

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/02_remote_agent_server/17_convo_with_agent_sandbox_server.py)

Run from the repository root: `uv run python examples/02_remote_agent_server/17_convo_with_agent_sandbox_server.py`.

## 05 skills and plugins

### main

Example: Loading Skills from Disk (AgentSkills Standard)

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/05_skills_and_plugins/01_loading_agentskills/main.py)

Run from the repository root: `uv run python examples/05_skills_and_plugins/01_loading_agentskills/main.py`.

### main

Example: Loading and Managing Plugins

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/05_skills_and_plugins/02_loading_plugins/main.py)

Run from the repository root: `uv run python examples/05_skills_and_plugins/02_loading_plugins/main.py`.

### main

Example: Installing and Managing Skills

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/05_skills_and_plugins/03_managing_installed_skills/main.py)

Run from the repository root: `uv run python examples/05_skills_and_plugins/03_managing_installed_skills/main.py`.

### main

Example: Mixed Marketplace with Local and Remote Skills

[Source](https://github.com/Praxiss-Lab/praxis-sdk/blob/main/examples/05_skills_and_plugins/04_mixed_marketplace_skills/main.py)

Run from the repository root: `uv run python examples/05_skills_and_plugins/04_mixed_marketplace_skills/main.py`.

