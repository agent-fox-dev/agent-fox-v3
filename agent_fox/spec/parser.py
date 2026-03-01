"""Task definition parser: parse tasks.md and prd.md dependency tables.

Requirements: 02-REQ-2.1, 02-REQ-2.2, 02-REQ-2.3, 02-REQ-2.4,
              02-REQ-2.E1, 02-REQ-2.E2
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SubtaskDef:
    """A single nested subtask within a task group."""

    id: str  # e.g., "1.2"
    title: str  # subtask description text
    completed: bool  # checkbox state


@dataclass(frozen=True)
class TaskGroupDef:
    """A parsed top-level task group from tasks.md."""

    number: int  # group number (1, 2, 3, ...)
    title: str  # group title text
    optional: bool  # True if marked with *
    completed: bool  # True if checkbox is [x]
    subtasks: tuple[SubtaskDef, ...]  # nested subtasks
    body: str  # full raw text of the group


@dataclass(frozen=True)
class CrossSpecDep:
    """A cross-spec dependency declaration from a prd.md table."""

    from_spec: str  # source spec name
    from_group: int  # source group number
    to_spec: str  # target spec name
    to_group: int  # target group number


def parse_tasks(tasks_path: Path) -> list[TaskGroupDef]:
    """Parse a tasks.md file into a list of task group definitions.

    Args:
        tasks_path: Path to the tasks.md file.

    Returns:
        List of TaskGroupDef in document order.
    """
    raise NotImplementedError("parse_tasks not yet implemented")


def parse_cross_deps(prd_path: Path) -> list[CrossSpecDep]:
    """Parse cross-spec dependency table from a spec's prd.md.

    Args:
        prd_path: Path to the spec's prd.md file.

    Returns:
        List of CrossSpecDep declarations. Empty if no table found.
    """
    raise NotImplementedError("parse_cross_deps not yet implemented")
