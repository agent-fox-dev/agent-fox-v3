"""Fast-mode filter: remove optional nodes and rewire dependencies.

Requirements: 02-REQ-5.1, 02-REQ-5.2, 02-REQ-5.3
"""

from __future__ import annotations

from agent_fox.graph.types import TaskGraph


def apply_fast_mode(graph: TaskGraph) -> TaskGraph:
    """Remove optional nodes and rewire dependencies.

    For each optional node B with predecessors {A1, A2} and
    successors {C1, C2}, add edges A_i -> C_j for all combinations,
    then remove B and its edges. B's status is set to SKIPPED.

    Args:
        graph: The full task graph.

    Returns:
        A new TaskGraph with optional nodes removed and dependencies
        rewired. The skipped nodes are retained in the graph with
        SKIPPED status but excluded from the ordering.
    """
    raise NotImplementedError("apply_fast_mode not yet implemented")
