"""Tests for duration-based ordering in graph_sync and config.

Test Spec: TS-41-1, TS-41-2, TS-41-3, TS-41-4, TS-41-16, TS-41-17, TS-41-18
Edge Cases: TS-41-E2, TS-41-E6, TS-41-E7
Requirements: 41-REQ-1.1 through 41-REQ-1.E2, 41-REQ-5.1, 41-REQ-5.2, 41-REQ-5.E1
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# TS-41-1, TS-41-2, TS-41-3: order_by_duration()
# ---------------------------------------------------------------------------


class TestOrderByDuration:
    """Tests for the order_by_duration() sorting function.

    Test Spec: TS-41-1, TS-41-2, TS-41-3
    """

    def test_descending_duration_ordering(self) -> None:
        """TS-41-1: Tasks sorted by predicted duration descending.

        Requirement: 41-REQ-1.1
        """
        from agent_fox.routing.duration import order_by_duration

        result = order_by_duration(["a", "b", "c"], {"a": 100, "b": 500, "c": 300})
        assert result == ["b", "c", "a"]

    def test_alphabetical_tie_breaking(self) -> None:
        """TS-41-2: Alphabetical tie-breaking when durations are equal.

        Requirement: 41-REQ-1.2
        """
        from agent_fox.routing.duration import order_by_duration

        result = order_by_duration(
            ["alpha", "beta", "gamma"],
            {"alpha": 200, "beta": 200, "gamma": 500},
        )
        assert result == ["gamma", "alpha", "beta"]

    def test_tasks_without_hints_placed_last(self) -> None:
        """TS-41-3: Tasks without hints placed after hinted tasks.

        Requirement: 41-REQ-1.3
        """
        from agent_fox.routing.duration import order_by_duration

        result = order_by_duration(["d", "c", "b", "a"], {"a": 100, "c": 300})
        assert result == ["c", "a", "b", "d"]


# ---------------------------------------------------------------------------
# TS-41-4, TS-41-18: ready_tasks() with duration hints
# ---------------------------------------------------------------------------


class TestReadyTasksOrdering:
    """Tests for GraphSync.ready_tasks() with duration hints.

    Test Spec: TS-41-4, TS-41-18
    """

    def test_no_hints_returns_alphabetical(self) -> None:
        """TS-41-4: Alphabetical order when no duration hints provided.

        Requirement: 41-REQ-1.4
        """
        from agent_fox.engine.graph_sync import GraphSync

        gs = GraphSync({"c": "pending", "a": "pending", "b": "pending"}, {})
        result = gs.ready_tasks(duration_hints=None)
        assert result == ["a", "b", "c"]

    def test_duration_hints_passed_to_ready_tasks(self) -> None:
        """TS-41-18: ready_tasks uses duration hints for ordering.

        Requirement: 41-REQ-5.3
        """
        from agent_fox.engine.graph_sync import GraphSync

        gs = GraphSync({"a": "pending", "b": "pending", "c": "pending"}, {})
        result = gs.ready_tasks(duration_hints={"a": 500, "b": 100, "c": 300})
        assert result == ["a", "c", "b"]

    def test_empty_hints_dict_treated_as_none(self) -> None:
        """TS-41-E2: Empty hints dict treated as None (alphabetical).

        Requirement: 41-REQ-1.E2
        """
        from agent_fox.engine.graph_sync import GraphSync

        gs = GraphSync({"c": "pending", "a": "pending", "b": "pending"}, {})
        result = gs.ready_tasks(duration_hints={})
        assert result == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# TS-41-16: PlanningConfig Defaults
# ---------------------------------------------------------------------------


class TestPlanningConfig:
    """Tests for PlanningConfig duration-related fields.

    Test Spec: TS-41-16, TS-41-17
    """

    def test_planning_config_defaults(self) -> None:
        """TS-41-16: Default PlanningConfig values.

        Requirement: 41-REQ-5.1
        """
        from agent_fox.core.config import PlanningConfig

        config = PlanningConfig()
        assert config.duration_ordering is True
        assert config.min_outcomes_for_historical == 10
        assert config.min_outcomes_for_regression == 30

    def test_duration_ordering_disabled_returns_none(self) -> None:
        """TS-41-17: No duration hints computed when ordering is disabled.

        Requirement: 41-REQ-5.2

        Note: This test verifies the config flag. Full orchestrator integration
        is tested in task group 3.
        """
        from agent_fox.core.config import PlanningConfig

        config = PlanningConfig(duration_ordering=False)
        assert config.duration_ordering is False


# ---------------------------------------------------------------------------
# TS-41-E6, TS-41-E7: Config Clamping
# ---------------------------------------------------------------------------


class TestConfigClamping:
    """Tests for PlanningConfig value clamping.

    Test Spec: TS-41-E6, TS-41-E7
    """

    def test_historical_min_clamped_low(self) -> None:
        """TS-41-E6: min_outcomes_for_historical clamped to 1 when too low.

        Requirement: 41-REQ-5.E1
        """
        from agent_fox.core.config import PlanningConfig

        c = PlanningConfig(min_outcomes_for_historical=0)
        assert c.min_outcomes_for_historical == 1

    def test_historical_min_clamped_high(self) -> None:
        """TS-41-E6: min_outcomes_for_historical clamped to 1000 when too high.

        Requirement: 41-REQ-5.E1
        """
        from agent_fox.core.config import PlanningConfig

        c = PlanningConfig(min_outcomes_for_historical=5000)
        assert c.min_outcomes_for_historical == 1000

    def test_regression_min_clamped_low(self) -> None:
        """TS-41-E7: min_outcomes_for_regression clamped to 5 when too low.

        Requirement: 41-REQ-5.E1
        """
        from agent_fox.core.config import PlanningConfig

        c = PlanningConfig(min_outcomes_for_regression=2)
        assert c.min_outcomes_for_regression == 5

    def test_regression_min_clamped_high(self) -> None:
        """TS-41-E7: min_outcomes_for_regression clamped to 10000 when too high.

        Requirement: 41-REQ-5.E1
        """
        from agent_fox.core.config import PlanningConfig

        c = PlanningConfig(min_outcomes_for_regression=50000)
        assert c.min_outcomes_for_regression == 10000
