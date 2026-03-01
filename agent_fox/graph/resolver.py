"""Dependency resolver: topological sort with cycle detection.

Requirements: 02-REQ-4.1, 02-REQ-4.2, 02-REQ-3.E2
"""

from __future__ import annotations

from agent_fox.graph.types import TaskGraph


def resolve_order(graph: TaskGraph) -> list[str]:
    """Compute a topological ordering of the task graph.

    Uses Kahn's algorithm. Ties are broken by spec prefix (ascending)
    then group number (ascending) for deterministic output.

    Args:
        graph: TaskGraph with nodes and edges.

    Returns:
        List of node IDs in execution order.

    Raises:
        PlanError: If the graph contains a cycle, listing involved nodes.
    """
    raise NotImplementedError("resolve_order not yet implemented")
