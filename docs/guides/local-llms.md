# Local LLMs

Praxis SDK works with local model servers such as Ollama, LM Studio, vLLM and
llama.cpp through their OpenAI-compatible endpoints.

```python
from praxis.sdk import LLM

llm = LLM(
    model="openai/qwen3-coder",              # provider prefix + model served locally
    base_url="http://127.0.0.1:11434/v1",    # Ollama; LM Studio uses :1234/v1
    api_key="local",                         # most local servers accept any value
)
```

## Context window

Agents need a large context. Praxis SDK refuses models whose context window is below
**16,384 tokens**. Increase it in your server configuration, for example:

**Ollama**

```sh
OLLAMA_CONTEXT_LENGTH=32768 ollama serve
```

**LM Studio:** set *Context Length* to 32768 or more when loading the model.

**vLLM**

```sh
vllm serve <model> --max-model-len 32768
```

Only if you understand the consequences, the check can be disabled with
`ALLOW_SHORT_CONTEXT_WINDOWS=true`.

## Tips

- Prefer models trained for tool calling; smaller models may loop or produce invalid calls.
- Use the [stuck detector and condenser](../concepts/conversations.md#context-management) for long tasks.
- When the agent runs inside Docker, `127.0.0.1` refers to the container: use the host address instead.
