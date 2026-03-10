"""Phase 2 report rendering and combined report.

Requirements: 31-REQ-9.*
"""

from __future__ import annotations

from rich.console import Console

from agent_fox.fix.fix import FixResult
from agent_fox.fix.improve import ImproveResult


def render_combined_report(
    fix_result: FixResult,
    improve_result: ImproveResult | None,
    total_cost: float,
    console: Console,
) -> None:
    """Render the combined Phase 1 + Phase 2 report."""
    raise NotImplementedError


def build_combined_json(
    fix_result: FixResult,
    improve_result: ImproveResult | None,
    total_cost: float,
) -> dict:
    """Build the JSONL-compatible dict for the combined report."""
    raise NotImplementedError
