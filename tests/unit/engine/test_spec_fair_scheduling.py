"""Tests for spec-fair round-robin task scheduling.

Test Spec: TS-69-1 through TS-69-10, TS-69-E1 through TS-69-E4
Requirements: 69-REQ-1.1 through 69-REQ-3.E1
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# TS-69-1 through TS-69-7: _interleave_by_spec()
# ---------------------------------------------------------------------------


class TestInterleaveBySpec:
    """Tests for the _interleave_by_spec() helper function.

    Test Spec: TS-69-1, TS-69-2, TS-69-3, TS-69-4, TS-69-5, TS-69-6, TS-69-7
    """

    def test_multi_spec_round_robin_ordering(self) -> None:
        """TS-69-1: Tasks from multiple specs are interleaved round-robin.

        Requirements: 69-REQ-1.1
        """
        from agent_fox.engine.graph_sync import _interleave_by_spec

        result = _interleave_by_spec(["65_foo:1", "67_bar:1", "67_bar:2", "68_baz:1"])
        assert result == ["65_foo:1", "67_bar:1", "68_baz:1", "67_bar:2"]

    def test_spec_number_ascending_order(self) -> None:
        """TS-69-2: Spec groups are ordered by numeric prefix ascending.

        Requirements: 69-REQ-1.2
        """
        from agent_fox.engine.graph_sync import _interleave_by_spec

        result = _interleave_by_spec(["68_later:1", "65_earlier:1"])
        assert result == ["65_earlier:1", "68_later:1"]

    def test_single_spec_alphabetical(self) -> None:
        """TS-69-3: Single-spec ready tasks are sorted alphabetically.

        Requirements: 69-REQ-1.3
        """
        from agent_fox.engine.graph_sync import _interleave_by_spec

        result = _interleave_by_spec(["42_spec:3", "42_spec:1", "42_spec:2"])
        assert result == ["42_spec:1", "42_spec:2", "42_spec:3"]

    def test_non_numeric_spec_prefix_sorts_last(self) -> None:
        """TS-69-4: Specs without numeric prefixes sort after numbered specs.

        Requirements: 69-REQ-1.4
        """
        from agent_fox.engine.graph_sync import _interleave_by_spec

        result = _interleave_by_spec(["no_number:1", "05_numbered:1"])
        assert result == ["05_numbered:1", "no_number:1"]

    def test_duration_hints_within_spec_group(self) -> None:
        """TS-69-5: Duration hints order tasks within spec group by duration descending.

        Requirements: 69-REQ-2.1
        """
        from agent_fox.engine.graph_sync import _interleave_by_spec

        result = _interleave_by_spec(
            ["42_spec:1", "42_spec:2", "42_spec:3"],
            duration_hints={"42_spec:1": 100, "42_spec:2": 500, "42_spec:3": 300},
        )
        assert result == ["42_spec:2", "42_spec:3", "42_spec:1"]

    def test_duration_hints_do_not_override_cross_spec_fairness(self) -> None:
        """TS-69-6: Duration hints do not override cross-spec round-robin ordering.

        Requirements: 69-REQ-2.2
        """
        from agent_fox.engine.graph_sync import _interleave_by_spec

        result = _interleave_by_spec(
            ["10_fast:1", "20_slow:1"],
            duration_hints={"10_fast:1": 100, "20_slow:1": 99999},
        )
        assert result[0] == "10_fast:1"
        assert result[1] == "20_slow:1"

    def test_duration_hints_partial_coverage_within_spec(self) -> None:
        """TS-69-7: Hinted tasks come before unhinted tasks within a spec group.

        Requirements: 69-REQ-2.3
        """
        from agent_fox.engine.graph_sync import _interleave_by_spec

        result = _interleave_by_spec(
            ["42_spec:1", "42_spec:2", "42_spec:3"],
            duration_hints={"42_spec:1": 200, "42_spec:3": 500},
        )
        assert result == ["42_spec:3", "42_spec:1", "42_spec:2"]


# ---------------------------------------------------------------------------
# TS-69-8, TS-69-9: _spec_name()
# ---------------------------------------------------------------------------


class TestSpecNameExtraction:
    """Tests for the _spec_name() helper function.

    Test Spec: TS-69-8, TS-69-9
    """

    def test_spec_name_extraction_simple(self) -> None:
        """TS-69-8: Spec name is extracted as everything before the first colon.

        Requirements: 69-REQ-3.1
        """
        from agent_fox.engine.graph_sync import _spec_name

        assert _spec_name("67_quality_gate:2") == "67_quality_gate"

    def test_spec_name_extraction_multi_colon(self) -> None:
        """TS-69-9: Only the first colon is used for splitting.

        Requirements: 69-REQ-3.2
        """
        from agent_fox.engine.graph_sync import _spec_name

        assert _spec_name("67_quality_gate:1:auditor") == "67_quality_gate"


# ---------------------------------------------------------------------------
# TS-69-10: GraphSync.ready_tasks() integration
# ---------------------------------------------------------------------------


class TestReadyTasksIntegration:
    """Integration tests for GraphSync.ready_tasks() with spec-fair ordering.

    Test Spec: TS-69-10
    """

    def test_ready_tasks_multi_spec_graph(self) -> None:
        """TS-69-10: ready_tasks() returns spec-fair ordering for multi-spec graph.

        Requirements: 69-REQ-1.1, 69-REQ-2.2
        """
        from agent_fox.engine.graph_sync import GraphSync

        gs = GraphSync({"67_qg:0": "pending", "68_cfg:0": "pending"}, {})
        result = gs.ready_tasks()
        assert result == ["67_qg:0", "68_cfg:0"]


# ---------------------------------------------------------------------------
# TS-69-E1 through TS-69-E4: Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Edge case tests for spec-fair scheduling.

    Test Spec: TS-69-E1, TS-69-E2, TS-69-E3, TS-69-E4
    """

    def test_single_spec_identity(self) -> None:
        """TS-69-E1: Single-spec result equals sorted(input).

        Requirements: 69-REQ-1.E1
        """
        from agent_fox.engine.graph_sync import _interleave_by_spec

        ready = ["42_spec:3", "42_spec:1", "42_spec:0"]
        result = _interleave_by_spec(ready)
        assert result == sorted(ready)

    def test_empty_list(self) -> None:
        """TS-69-E2: Empty input returns empty output.

        Requirements: 69-REQ-1.E2
        """
        from agent_fox.engine.graph_sync import _interleave_by_spec

        assert _interleave_by_spec([]) == []

    def test_duration_hints_single_spec(self) -> None:
        """TS-69-E3: Duration ordering within a single spec.

        Requirements: 69-REQ-2.E1
        """
        from agent_fox.engine.graph_sync import _interleave_by_spec

        result = _interleave_by_spec(
            ["42_spec:1", "42_spec:2"],
            duration_hints={"42_spec:1": 100, "42_spec:2": 500},
        )
        assert result == ["42_spec:2", "42_spec:1"]

    def test_no_colon_node_id(self) -> None:
        """TS-69-E4: Node ID with no colon uses full ID as spec name.

        Requirements: 69-REQ-3.E1
        """
        from agent_fox.engine.graph_sync import _spec_name

        assert _spec_name("orphan_node") == "orphan_node"
