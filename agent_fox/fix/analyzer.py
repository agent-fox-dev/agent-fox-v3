"""Analyzer module for Phase 2 auto-improve.

Builds analyzer prompts, parses structured JSON responses, filters
improvements by confidence and tier priority, and queries the oracle
for project knowledge context.

Requirements: 31-REQ-3.*, 31-REQ-4.*
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent_fox.core.config import AgentFoxConfig


@dataclass(frozen=True)
class Improvement:
    """A single improvement suggestion from the analyzer."""

    id: str
    tier: str  # "quick_win" | "structural" | "design_level"
    title: str
    description: str
    files: list[str]
    impact: str  # "low" | "medium" | "high"
    confidence: str  # "high" | "medium" | "low"


@dataclass
class AnalyzerResult:
    """Parsed output from the analyzer session."""

    improvements: list[Improvement]
    summary: str
    diminishing_returns: bool
    raw_response: str = ""  # for debugging


def build_analyzer_prompt(
    project_root: Path,
    config: AgentFoxConfig,
    *,
    oracle_context: str = "",
    review_context: str = "",
    phase1_diff: str = "",
    previous_pass_result: str = "",
) -> tuple[str, str]:
    """Build the system prompt and task prompt for the analyzer.

    Returns (system_prompt, task_prompt).
    """
    raise NotImplementedError


def parse_analyzer_response(response: str) -> AnalyzerResult:
    """Parse the analyzer's JSON response into an AnalyzerResult."""
    raise NotImplementedError


def filter_improvements(
    improvements: list[Improvement],
) -> list[Improvement]:
    """Filter out low-confidence improvements and sort by tier priority."""
    raise NotImplementedError


def query_oracle_context(config: AgentFoxConfig) -> str:
    """Query the oracle for project knowledge context."""
    raise NotImplementedError


def load_review_context(project_root: Path) -> str:
    """Load existing skeptic/verifier findings from DuckDB."""
    raise NotImplementedError
