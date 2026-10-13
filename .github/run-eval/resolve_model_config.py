"""Resolve explicit model IDs locally without downloading upstream code."""

from typing import Any


MODELS: dict[str, Any] = {}


def find_models_by_id(model_ids: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "id": model_id,
            "display_name": model_id,
            "llm_config": {"model": model_id},
        }
        for model_id in model_ids
    ]
