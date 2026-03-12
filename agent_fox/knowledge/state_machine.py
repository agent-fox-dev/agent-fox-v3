"""In-memory buffer for facts during an orchestrator run.

Facts are accumulated via add_fact() and written to DuckDB in
batch via flush(). The state machine does not own the DuckDB
connection -- it delegates to MemoryStore.

Requirements: 39-REQ-4.1, 39-REQ-4.2, 39-REQ-4.3, 39-REQ-4.4,
              39-REQ-4.5, 39-REQ-4.6, 39-REQ-4.E1
"""

from __future__ import annotations

from agent_fox.knowledge.facts import Fact
from agent_fox.knowledge.store import MemoryStore


class KnowledgeStateMachine:
    """In-memory buffer for facts during an orchestrator run.

    Facts are accumulated via add_fact() and written to DuckDB in
    batch via flush(). The state machine does not own the DuckDB
    connection -- it delegates to MemoryStore.

    Full implementation in task group 4.
    """

    def __init__(self, store: MemoryStore) -> None:
        """Initialize with a MemoryStore for DuckDB access."""
        self._store = store
        self._buffer: list[Fact] = []

    @property
    def pending(self) -> list[Fact]:
        """Return a copy of buffered facts not yet flushed."""
        return list(self._buffer)

    def add_fact(self, fact: Fact) -> None:
        """Buffer a fact for later flushing. No DuckDB write."""
        self._buffer.append(fact)

    def flush(self) -> int:
        """Write all buffered facts to DuckDB via MemoryStore.

        Returns the number of facts flushed. Clears the buffer on
        success. On partial failure, removes successfully-written
        facts from the buffer and re-raises the error.
        """
        raise NotImplementedError("Full implementation in task group 4")
