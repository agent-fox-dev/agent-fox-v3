"""Phase 2 improve loop for auto-improve.

Orchestrates analyzer, coder, verifier sessions per pass, manages
termination conditions, cost tracking, and rollback.

Requirements: 31-REQ-5.* through 31-REQ-8.*
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from agent_fox.core.config import AgentFoxConfig
from agent_fox.fix.checks import CheckDescriptor


class ImproveTermination(StrEnum):
    """Reason the improve loop terminated."""

    CONVERGED = "converged"
    PASS_LIMIT = "pass_limit"
    COST_LIMIT = "cost_limit"
    VERIFIER_FAIL = "verifier_fail"
    INTERRUPTED = "interrupted"
    ANALYZER_ERROR = "analyzer_error"
    CODER_ERROR = "coder_error"


@dataclass
class VerifierVerdict:
    """Parsed verifier verdict."""

    quality_gates: str  # "PASS" or "FAIL"
    improvement_valid: bool
    verdict: str  # "PASS" or "FAIL"
    evidence: str


@dataclass
class ImprovePassResult:
    """Result of a single improvement pass."""

    pass_number: int
    improvements_applied: int
    improvements_by_tier: dict[str, int]
    verifier_verdict: str  # "PASS" or "FAIL"
    analyzer_cost: float
    coder_cost: float
    verifier_cost: float
    rolled_back: bool


@dataclass
class ImproveResult:
    """Result of the entire Phase 2 improve loop."""

    passes_completed: int
    max_passes: int
    total_improvements: int
    improvements_by_tier: dict[str, int]
    verifier_pass_count: int
    verifier_fail_count: int
    sessions_consumed: int
    total_cost: float
    termination_reason: ImproveTermination
    pass_results: list[ImprovePassResult] = field(default_factory=list)


def parse_verifier_verdict(response: str) -> VerifierVerdict:
    """Parse the verifier's JSON verdict."""
    raise NotImplementedError


def rollback_improvement_pass(project_root: Path) -> None:
    """Roll back the most recent commit via git reset --hard HEAD~1."""
    raise NotImplementedError


def discard_partial_changes(project_root: Path) -> None:
    """Discard uncommitted changes via git checkout -- ."""
    raise NotImplementedError


async def run_improve_loop(
    project_root: Path,
    config: AgentFoxConfig,
    checks: list[CheckDescriptor] | None = None,
    max_passes: int = 3,
    remaining_budget: float | None = None,
    phase1_diff: str = "",
    session_runner: Callable[..., Awaitable[tuple[float, str]]] | None = None,
) -> ImproveResult:
    """Run the iterative improvement loop (Phase 2)."""
    raise NotImplementedError
