"""Graph builder: construct TaskGraph from discovered specs and parsed tasks.

Requirements: 02-REQ-3.1, 02-REQ-3.2, 02-REQ-3.E1
"""

from __future__ import annotations

from agent_fox.graph.types import TaskGraph
from agent_fox.spec.discovery import SpecInfo
from agent_fox.spec.parser import CrossSpecDep, TaskGroupDef


def build_graph(
    specs: list[SpecInfo],
    task_groups: dict[str, list[TaskGroupDef]],
    cross_deps: list[CrossSpecDep],
) -> TaskGraph:
    """Construct a TaskGraph from discovered specs and parsed tasks.

    1. Create a Node for each task group.
    2. Add intra-spec edges (group N depends on N-1).
    3. Add cross-spec edges from dependency declarations.
    4. Validate: no dangling references.

    Args:
        specs: Discovered spec metadata.
        task_groups: Mapping of spec_name -> list of TaskGroupDef.
        cross_deps: Cross-spec dependency declarations.

    Returns:
        TaskGraph with nodes and edges but no ordering yet.

    Raises:
        PlanError: If dangling cross-spec references found.
    """
    raise NotImplementedError("build_graph not yet implemented")
