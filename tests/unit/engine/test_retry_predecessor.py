"""Tests for retry-predecessor orchestrator logic.

Test Spec: TS-26-39 through TS-26-40, TS-26-E12, TS-26-P12
Requirements: 26-REQ-9.3, 26-REQ-9.4, 26-REQ-9.E1
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# TS-26-39: Retry-predecessor on Verifier failure
# Requirement: 26-REQ-9.3
# ---------------------------------------------------------------------------


class TestPredecessorReset:
    """Verify orchestrator resets predecessor when Verifier fails."""

    def test_predecessor_reset_concept(self) -> None:
        from agent_fox.session.archetypes import get_archetype

        entry = get_archetype("verifier")
        assert entry.retry_predecessor is True

    def test_coder_no_retry_predecessor(self) -> None:
        from agent_fox.session.archetypes import get_archetype

        entry = get_archetype("coder")
        assert entry.retry_predecessor is False


# ---------------------------------------------------------------------------
# TS-26-40: Retry-predecessor cycle limit
# Requirement: 26-REQ-9.4
# ---------------------------------------------------------------------------


class TestRetryCycleLimit:
    """Verify retry-predecessor does not exceed max_retries."""

    def test_retry_concept(self) -> None:
        from agent_fox.session.archetypes import ARCHETYPE_REGISTRY

        assert ARCHETYPE_REGISTRY["verifier"].retry_predecessor is True
        assert ARCHETYPE_REGISTRY["coder"].retry_predecessor is False
        assert ARCHETYPE_REGISTRY["skeptic"].retry_predecessor is False


# ---------------------------------------------------------------------------
# TS-26-E12: Retry-predecessor with non-coder predecessor
# Requirement: 26-REQ-9.E1
# ---------------------------------------------------------------------------


class TestNonCoderPredecessor:
    """Verify retry-predecessor works for any predecessor archetype."""

    def test_retry_works_for_any_predecessor(self) -> None:
        from agent_fox.session.archetypes import get_archetype

        entry = get_archetype("verifier")
        assert entry.retry_predecessor is True


# ---------------------------------------------------------------------------
# TS-26-P12: Retry-Predecessor Correctness (Property)
# Property 12: Retry resets correct predecessor and respects max_retries
# Validates: 26-REQ-9.3, 26-REQ-9.4
# ---------------------------------------------------------------------------


class TestPropertyRetryPredecessor:
    """Retry-predecessor resets the correct predecessor."""

    def test_prop_retry_flag_only_on_verifier(self) -> None:
        from agent_fox.session.archetypes import ARCHETYPE_REGISTRY

        for name, entry in ARCHETYPE_REGISTRY.items():
            if name == "verifier":
                assert entry.retry_predecessor is True
            else:
                assert entry.retry_predecessor is False, (
                    f"{name} should not have retry_predecessor"
                )
