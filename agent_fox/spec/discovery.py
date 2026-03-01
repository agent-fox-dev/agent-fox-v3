"""Specification discovery: scan .specs/ for valid spec folders.

Requirements: 02-REQ-1.1, 02-REQ-1.2, 02-REQ-1.3, 02-REQ-1.E1, 02-REQ-1.E2
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SpecInfo:
    """Metadata about a discovered specification folder."""

    name: str  # e.g., "01_core_foundation"
    prefix: int  # e.g., 1
    path: Path  # e.g., Path(".specs/01_core_foundation")
    has_tasks: bool  # whether tasks.md exists
    has_prd: bool  # whether prd.md exists


def discover_specs(
    specs_dir: Path,
    filter_spec: str | None = None,
) -> list[SpecInfo]:
    """Discover spec folders in the given directory.

    Args:
        specs_dir: Path to the .specs/ directory.
        filter_spec: If set, return only this spec (by name or prefix).

    Returns:
        List of SpecInfo sorted by numeric prefix.

    Raises:
        PlanError: If no specs found or filter matches nothing.
    """
    raise NotImplementedError("discover_specs not yet implemented")
