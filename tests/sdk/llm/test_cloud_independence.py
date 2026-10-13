import pytest

from openhands.sdk import LLM
from openhands.sdk.critic.impl.api.client import CriticClient
from openhands.sdk.llm import Message, TextContent


@pytest.mark.parametrize(
    "model,base_url",
    [
        ("openhands/claude-sonnet-4-5", None),
        ("openai/gpt-4o", "https://llm-proxy.app.all-hands.dev/v1"),
        ("openai/gpt-4o", "https://APP.OPENHANDS.DEV./v1"),
    ],
)
def test_hosted_cloud_transport_is_rejected_before_provider_call(
    monkeypatch, model, base_url
):
    calls = []
    monkeypatch.setattr(
        "openhands.sdk.llm.llm.litellm_completion", lambda **kw: calls.append(kw)
    )
    monkeypatch.setattr(
        "openhands.sdk.llm.llm.get_litellm_model_info", lambda *args, **kwargs: None
    )
    with pytest.raises(ValueError, match="self-hosted|OpenHands Cloud"):
        llm = LLM(model=model, base_url=base_url, api_key="private-test-key")
        llm.completion(
            messages=[Message(role="user", content=[TextContent(text="hello")])]
        )
    assert calls == []


def test_critic_default_is_local():
    assert CriticClient(api_key="test").server_url.startswith("http://127.0.0.1:")


def test_critic_rejects_hosted_endpoint():
    with pytest.raises(ValueError, match="OpenHands Cloud"):
        CriticClient(
            api_key="test", server_url="https://llm-proxy.app.all-hands.dev/vllm"
        ).classify_trace([])
