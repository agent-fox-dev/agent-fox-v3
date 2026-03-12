"""Property tests for project model.

Test Spec: TS-43-P1 (failure rate bounds)
Property: Property 1 from design.md
Validates: 43-REQ-1.1
"""

from __future__ import annotations

import uuid

import duckdb
from hypothesis import given, settings
from hypothesis import strategies as st

from agent_fox.knowledge.project_model import build_project_model


def _create_model_schema(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the minimum schema needed for project model tests."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS complexity_assessments (
            id              VARCHAR PRIMARY KEY,
            node_id         VARCHAR NOT NULL,
            spec_name       VARCHAR NOT NULL,
            task_group      INTEGER NOT NULL,
            predicted_tier  VARCHAR NOT NULL,
            confidence      FLOAT NOT NULL,
            assessment_method VARCHAR NOT NULL,
            feature_vector  JSON NOT NULL,
            tier_ceiling    VARCHAR NOT NULL,
            created_at      TIMESTAMP NOT NULL DEFAULT current_timestamp
        );

        CREATE TABLE IF NOT EXISTS execution_outcomes (
            id                  VARCHAR PRIMARY KEY,
            assessment_id       VARCHAR NOT NULL REFERENCES complexity_assessments(id),
            actual_tier         VARCHAR NOT NULL,
            total_tokens        INTEGER NOT NULL,
            total_cost          FLOAT NOT NULL,
            duration_ms         INTEGER NOT NULL,
            attempt_count       INTEGER NOT NULL,
            escalation_count    INTEGER NOT NULL,
            outcome             VARCHAR NOT NULL,
            files_touched_count INTEGER NOT NULL,
            created_at          TIMESTAMP NOT NULL DEFAULT current_timestamp
        );

        CREATE TABLE IF NOT EXISTS review_findings (
            id              UUID PRIMARY KEY,
            severity        TEXT NOT NULL,
            description     TEXT NOT NULL,
            requirement_ref TEXT,
            spec_name       TEXT NOT NULL,
            task_group      TEXT NOT NULL,
            session_id      TEXT NOT NULL,
            superseded_by   TEXT,
            created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS drift_findings (
            id UUID PRIMARY KEY,
            severity VARCHAR NOT NULL,
            description VARCHAR NOT NULL,
            spec_ref VARCHAR,
            artifact_ref VARCHAR,
            spec_name VARCHAR NOT NULL,
            task_group VARCHAR NOT NULL,
            session_id VARCHAR NOT NULL,
            superseded_by UUID,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


def _insert_outcome(
    conn: duckdb.DuckDBPyConnection,
    spec_name: str,
    cost: float,
    duration_ms: int,
    outcome: str,
) -> None:
    """Insert an assessment+outcome pair."""
    aid = str(uuid.uuid4())
    fv = (
        '{"subtask_count": 5, "spec_word_count": 200, '
        '"has_property_tests": false, "edge_case_count": 1, '
        '"dependency_count": 0, "archetype": "coder"}'
    )
    conn.execute(
        """INSERT INTO complexity_assessments
           (id, node_id, spec_name, task_group, predicted_tier,
            confidence, assessment_method, feature_vector, tier_ceiling)
           VALUES (?, ?, ?, 1, 'STANDARD', 0.8, 'heuristic', ?, 'MAX')""",
        [aid, f"{spec_name}/1", spec_name, fv],
    )
    conn.execute(
        """INSERT INTO execution_outcomes
           (id, assessment_id, actual_tier, total_tokens, total_cost,
            duration_ms, attempt_count, escalation_count, outcome,
            files_touched_count)
           VALUES (?, ?, 'STANDARD', 1000, ?, ?, 1, 0, ?, 3)""",
        [str(uuid.uuid4()), aid, cost, duration_ms, outcome],
    )


# Strategy: generate a list of (spec_name, cost, duration, outcome) tuples
outcome_strategy = st.sampled_from(["completed", "failed", "error"])
spec_name_strategy = st.sampled_from(["spec_a", "spec_b", "spec_c"])

session_entry = st.tuples(
    spec_name_strategy,
    st.floats(min_value=0.01, max_value=100.0),
    st.integers(min_value=100, max_value=1_000_000),
    outcome_strategy,
)


class TestFailureRateBounds:
    """TS-43-P1: SpecMetrics failure_rate is always in [0.0, 1.0].

    Property: Property 1 from design.md
    Validates: 43-REQ-1.1
    """

    @given(entries=st.lists(session_entry, min_size=1, max_size=15))
    @settings(max_examples=50, deadline=2000)
    def test_failure_rate_in_bounds(
        self,
        entries: list[tuple[str, float, int, str]],
    ) -> None:
        """For any SpecMetrics, failure_rate is in [0.0, 1.0] and
        session_count >= 1."""
        conn = duckdb.connect(":memory:")
        _create_model_schema(conn)

        for spec_name, cost, duration, outcome in entries:
            _insert_outcome(conn, spec_name, cost, duration, outcome)

        model = build_project_model(conn)

        for spec_metrics in model.spec_outcomes.values():
            assert 0.0 <= spec_metrics.failure_rate <= 1.0
            assert spec_metrics.session_count >= 1
