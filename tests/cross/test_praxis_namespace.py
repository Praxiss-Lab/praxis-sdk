"""Canonical imports must preserve legacy model and registry identity."""

import importlib

import pytest


@pytest.mark.parametrize(
    "name",
    ["sdk", "sdk.llm.llm", "tools", "tools.terminal", "workspace", "agent_server"],
)
def test_canonical_namespace_shares_legacy_module(name):
    assert importlib.import_module(f"praxis.{name}") is importlib.import_module(
        f"openhands.{name}"
    )


def test_canonical_models_keep_serialization_identity():
    from praxis.sdk import LLM

    from openhands.sdk import LLM as LegacyLLM

    assert LLM is LegacyLLM
    llm = LLM(model="openai/gpt-4o", api_key="test-only")
    assert LegacyLLM.model_validate(llm.model_dump()).model == llm.model
