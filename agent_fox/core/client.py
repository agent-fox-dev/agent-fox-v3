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


def _check_vertex_deps() -> None:
    """Fail fast if the Vertex extras are missing."""
    try:
        import google.auth  # noqa: F401
    except ModuleNotFoundError:
        raise RuntimeError(
            "CLAUDE_CODE_USE_VERTEX=1 is set but google-auth is "
            "not installed. Run: pip install 'anthropic[vertex]'"
        ) from None


def _check_bedrock_deps() -> None:
    """Fail fast if the Bedrock extras are missing."""
    try:
        import boto3  # noqa: F401
    except ModuleNotFoundError:
        raise RuntimeError(
            "CLAUDE_CODE_USE_BEDROCK=1 is set but boto3 is "
            "not installed. Run: pip install 'anthropic[bedrock]'"
        ) from None


def create_anthropic_client() -> anthropic.Anthropic:
    """Return a synchronous Anthropic client for the current platform."""
    if os.environ.get("CLAUDE_CODE_USE_VERTEX") == "1":
        _check_vertex_deps()
        from anthropic import AnthropicVertex

        return AnthropicVertex()  # type: ignore[return-value]

    if os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1":
        _check_bedrock_deps()
        from anthropic import AnthropicBedrock

        return AnthropicBedrock()  # type: ignore[return-value]

    return anthropic.Anthropic()


def create_async_anthropic_client() -> anthropic.AsyncAnthropic:
    """Return an async Anthropic client for the current platform."""
    if os.environ.get("CLAUDE_CODE_USE_VERTEX") == "1":
        _check_vertex_deps()
        from anthropic import AsyncAnthropicVertex

        return AsyncAnthropicVertex()  # type: ignore[return-value]

    if os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1":
        _check_bedrock_deps()
        from anthropic import AsyncAnthropicBedrock

        return AsyncAnthropicBedrock()  # type: ignore[return-value]

    return anthropic.AsyncAnthropic()
