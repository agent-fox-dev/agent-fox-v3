"""AI model registry with pricing.

Stub: defines types and signatures only.
Full implementation in task group 2.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ModelTier(StrEnum):
    SIMPLE = "SIMPLE"
    STANDARD = "STANDARD"
    ADVANCED = "ADVANCED"


@dataclass(frozen=True)
class ModelEntry:
    model_id: str
    tier: ModelTier
    input_price_per_m: float  # USD per million input tokens
    output_price_per_m: float  # USD per million output tokens


# Stub: empty registry — tests will fail until task group 2 populates this
MODEL_REGISTRY: dict[str, ModelEntry] = {}

TIER_DEFAULTS: dict[ModelTier, str] = {}


def resolve_model(name: str) -> ModelEntry:
    """Resolve a tier name or model ID to a ModelEntry."""
    raise NotImplementedError("resolve_model not yet implemented")


def calculate_cost(input_tokens: int, output_tokens: int, model: ModelEntry) -> float:
    """Calculate estimated cost in USD."""
    raise NotImplementedError("calculate_cost not yet implemented")
