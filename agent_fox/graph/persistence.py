"""Plan persistence: serialize/deserialize TaskGraph to/from JSON.

Requirements: 02-REQ-6.1, 02-REQ-6.2, 02-REQ-6.3, 02-REQ-6.4, 02-REQ-6.E1
"""

from __future__ import annotations

from pathlib import Path

from agent_fox.graph.types import TaskGraph


def save_plan(graph: TaskGraph, plan_path: Path) -> None:
    """Serialize a TaskGraph to JSON and write to disk.

    Args:
        graph: The task graph to persist.
        plan_path: Path to the plan.json file.
    """
    raise NotImplementedError("save_plan not yet implemented")


def load_plan(plan_path: Path) -> TaskGraph | None:
    """Load a TaskGraph from a JSON plan file.

    Args:
        plan_path: Path to the plan.json file.

    Returns:
        The deserialized TaskGraph, or None if the file is missing
        or corrupted (with a logged warning).
    """
    raise NotImplementedError("load_plan not yet implemented")
