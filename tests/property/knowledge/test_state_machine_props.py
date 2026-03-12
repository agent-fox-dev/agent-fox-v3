"""Property tests for KnowledgeStateMachine flush conservation.

Test Spec: TS-39-P1
Requirements: 39-REQ-4.3
"""

from __future__ import annotations

import uuid

import duckdb
from hypothesis import given, settings
from hypothesis import strategies as st

from tests.unit.knowledge.conftest import create_schema


def _make_fact(content: str):  # -> Fact
    """Create a Fact with unique ID."""
    from agent_fox.knowledge.facts import Fact

    return Fact(
        id=str(uuid.uuid4()),
        content=content,
        category="decision",
        spec_name="test_spec",
        keywords=["test"],
        confidence=0.9,
        created_at="2026-01-01T00:00:00Z",
    )


class TestFlushConservation:
    """TS-39-P1: Adding N facts and flushing results in N DuckDB rows."""

    @given(n=st.integers(min_value=1, max_value=50))
    @settings(max_examples=20, deadline=None)
    def test_flush_conserves_count(self, n: int) -> None:
        from agent_fox.knowledge.state_machine import KnowledgeStateMachine
        from agent_fox.knowledge.store import MemoryStore

        conn = duckdb.connect(":memory:")
        create_schema(conn)

        import tempfile
        from pathlib import Path

        tmp = Path(tempfile.mkdtemp()) / "memory.jsonl"

        store = MemoryStore(jsonl_path=tmp, db_conn=conn)
        sm = KnowledgeStateMachine(store=store)

        facts = [_make_fact(f"Fact {i}") for i in range(n)]
        for f in facts:
            sm.add_fact(f)

        result = sm.flush()
        assert result == n
        assert sm.pending == []

        rows = conn.execute("SELECT COUNT(*) FROM memory_facts").fetchone()
        assert rows is not None
        assert rows[0] == n

        conn.close()
