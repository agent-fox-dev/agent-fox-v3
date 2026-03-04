"""Platform-aware Anthropic client factory.

Detects whether the runtime is configured for Vertex AI, Bedrock,
or direct Anthropic API access and returns the appropriate SDK client.

Detection order (first match wins):
1. CLAUDE_CODE_USE_VERTEX=1  → AnthropicVertex / AsyncAnthropicVertex
2. CLAUDE_CODE_USE_BEDROCK=1 → AnthropicBedrock / AsyncAnthropicBedrock
3. Otherwise                 → Anthropic / AsyncAnthropic

No API keys are passed explicitly — each SDK variant auto-loads its
own environment variables.
"""

from __future__ import annotations

import os

import anthropic


def create_anthropic_client() -> anthropic.Anthropic:
    """Return a synchronous Anthropic client for the current platform."""
    if os.environ.get("CLAUDE_CODE_USE_VERTEX") == "1":
        from anthropic import AnthropicVertex

        return AnthropicVertex()  # type: ignore[return-value]

    if os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1":
        from anthropic import AnthropicBedrock

        return AnthropicBedrock()  # type: ignore[return-value]

    return anthropic.Anthropic()


def create_async_anthropic_client() -> anthropic.AsyncAnthropic:
    """Return an async Anthropic client for the current platform."""
    if os.environ.get("CLAUDE_CODE_USE_VERTEX") == "1":
        from anthropic import AsyncAnthropicVertex

        return AsyncAnthropicVertex()  # type: ignore[return-value]

    if os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1":
        from anthropic import AsyncAnthropicBedrock

        return AsyncAnthropicBedrock()  # type: ignore[return-value]

    return anthropic.AsyncAnthropic()
