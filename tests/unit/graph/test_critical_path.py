"""Tests for critical path computation.

Test Spec: TS-39-23, TS-39-24, TS-39-25,
           TS-43-5, TS-43-6, TS-43-7, TS-43-E3, TS-43-E4
Requirements: 39-REQ-8.1, 39-REQ-8.2, 39-REQ-8.3,
              43-REQ-2.1, 43-REQ-2.2, 43-REQ-2.3, 43-REQ-2.E1, 43-REQ-2.E2
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# TS-39-23: Critical Path Computation
# ---------------------------------------------------------------------------


class TestCriticalPath:
    """TS-39-23, TS-39-24, TS-39-25: Critical path computation.

    Requirements: 39-REQ-8.1, 39-REQ-8.2, 39-REQ-8.3
    """

    def test_compute_critical_path(self) -> None:
        """TS-39-23: Critical path uses duration hints as weights.

        Requirement: 39-REQ-8.1
        """
        from agent_fox.graph.critical_path import compute_critical_path

        nodes = {"A": "pending", "B": "pending", "C": "pending"}
        edges = {"B": ["A"], "C": ["B"]}
        hints = {"A": 100, "B": 200, "C": 50}

        result = compute_critical_path(nodes, edges, hints)
        assert result.path == ["A", "B", "C"]
        assert result.total_duration_ms == 350

    def test_parallel_paths_picks_longest(self) -> None:
        """Critical path picks the longest of parallel paths."""
        from agent_fox.graph.critical_path import compute_critical_path

        # A -> B -> D (total 350) and A -> C -> D (total 250)
        nodes = {"A": "pending", "B": "pending", "C": "pending", "D": "pending"}
        edges = {"B": ["A"], "C": ["A"], "D": ["B", "C"]}
        hints = {"A": 100, "B": 200, "C": 100, "D": 50}

        result = compute_critical_path(nodes, edges, hints)
        assert result.total_duration_ms == 350
        assert result.path == ["A", "B", "D"]

    def test_tied_paths(self) -> None:
        """TS-39-25: All tied critical paths reported.

        Requirement: 39-REQ-8.3
        """
        from agent_fox.graph.critical_path import compute_critical_path

        # Diamond graph: A->B->D and A->C->D with equal durations
        nodes = {"A": "pending", "B": "pending", "C": "pending", "D": "pending"}
        edges = {"B": ["A"], "C": ["A"], "D": ["B", "C"]}
        hints = {"A": 100, "B": 200, "C": 200, "D": 50}

        result = compute_critical_path(nodes, edges, hints)
        assert result.total_duration_ms == 350

        all_paths = [result.path] + result.tied_paths
        assert ["A", "B", "D"] in all_paths
        assert ["A", "C", "D"] in all_paths

    def test_single_node(self) -> None:
        """Single node graph returns that node as critical path."""
        from agent_fox.graph.critical_path import compute_critical_path

        nodes = {"A": "pending"}
        edges: dict[str, list[str]] = {}
        hints = {"A": 100}

        result = compute_critical_path(nodes, edges, hints)
        assert result.path == ["A"]
        assert result.total_duration_ms == 100

    def test_status_output(self) -> None:
        """TS-39-24: Critical path available for status output.

        Requirement: 39-REQ-8.2
        """
        from agent_fox.graph.critical_path import (
            CriticalPathResult,
            format_critical_path,
        )

        result = CriticalPathResult(
            path=["A", "B", "C"],
            total_duration_ms=350,
            tied_paths=[],
        )
        output = format_critical_path(result)
        assert "critical path" in output.lower() or "Critical Path" in output


# ---------------------------------------------------------------------------
# Spec 43: Critical Path tests
# ---------------------------------------------------------------------------


class TestComputeCriticalPath:
    """TS-43-5, TS-43-6: Compute critical path.

    Requirements: 43-REQ-2.1, 43-REQ-2.3
    """

    def test_linear_chain(self) -> None:
        """TS-43-5: Critical path through a simple linear chain.

        Requirement: 43-REQ-2.1

        Nodes: A, B, C (linear chain A -> B -> C).
        Duration hints: A=100, B=200, C=300.
        """
        from agent_fox.graph.critical_path import compute_critical_path

        result = compute_critical_path(
            {"A": "pending", "B": "pending", "C": "pending"},
            {"A": [], "B": ["A"], "C": ["B"]},
            {"A": 100, "B": 200, "C": 300},
        )
        assert result.path == ["A", "B", "C"]
        assert result.total_duration_ms == 600
        assert result.tied_paths == []

    def test_tied_paths(self) -> None:
        """TS-43-6: Tied path detection in a diamond DAG.

        Requirement: 43-REQ-2.3

        Nodes: S, A, B, E. Edges: A depends on S, B depends on S,
        E depends on A and B. Duration hints: S=100, A=200, B=200, E=100.
        """
        from agent_fox.graph.critical_path import compute_critical_path

        result = compute_critical_path(
            {"S": "p", "A": "p", "B": "p", "E": "p"},
            {"S": [], "A": ["S"], "B": ["S"], "E": ["A", "B"]},
            {"S": 100, "A": 200, "B": 200, "E": 100},
        )
        assert result.total_duration_ms == 400
        all_paths = [result.path] + result.tied_paths
        assert ["S", "A", "E"] in all_paths
        assert ["S", "B", "E"] in all_paths


class TestFormatCriticalPath:
    """TS-43-7: Format critical path output.

    Requirement: 43-REQ-2.2
    """

    def test_format_output(self) -> None:
        """TS-43-7: format_critical_path produces human-readable output.

        Requirement: 43-REQ-2.2
        """
        from agent_fox.graph.critical_path import (
            CriticalPathResult,
            format_critical_path,
        )

        result = CriticalPathResult(
            path=["A", "B", "C"],
            total_duration_ms=600,
            tied_paths=[],
        )
        output = format_critical_path(result)
        assert "== Critical Path ==" in output
        assert "A -> B -> C" in output
        assert "600ms" in output


class TestCriticalPathEdgeCases:
    """TS-43-E3, TS-43-E4: Critical path edge cases.

    Requirements: 43-REQ-2.E1, 43-REQ-2.E2
    """

    def test_empty_graph(self) -> None:
        """TS-43-E3: compute_critical_path handles empty graph.

        Requirement: 43-REQ-2.E1
        """
        from agent_fox.graph.critical_path import compute_critical_path

        result = compute_critical_path({}, {}, {})
        assert result.path == []
        assert result.total_duration_ms == 0

    def test_missing_duration(self) -> None:
        """TS-43-E4: Nodes without duration hints treated as 0ms.

        Requirement: 43-REQ-2.E2
        """
        from agent_fox.graph.critical_path import compute_critical_path

        result = compute_critical_path(
            {"A": "p", "B": "p"},
            {"A": [], "B": ["A"]},
            {"A": 100},
        )
        assert result.total_duration_ms == 100
