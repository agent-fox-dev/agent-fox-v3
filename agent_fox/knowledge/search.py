"""Vector similarity search over the memory_embeddings table.

Uses DuckDB's cosine distance for semantic search, returning
facts ranked by similarity with provenance metadata.

Requirements: 12-REQ-3.1, 12-REQ-3.2, 12-REQ-3.3, 12-REQ-3.E1,
              12-REQ-7.2
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import duckdb  # noqa: F401

from agent_fox.core.config import KnowledgeConfig

logger = logging.getLogger("agent_fox.knowledge.search")


@dataclass(frozen=True)
class SearchResult:
    """A single result from vector similarity search."""

    fact_id: str
    content: str
    category: str
    spec_name: str
    session_id: str | None
    commit_sha: str | None
    similarity: float


class VectorSearch:
    """Vector similarity search over the memory_embeddings table.

    Uses DuckDB's VSS extension for cosine similarity search over
    the HNSW index on memory_embeddings.embedding.
    """

    def __init__(
        self,
        conn: duckdb.DuckDBPyConnection,
        config: KnowledgeConfig,
    ) -> None:
        self._conn = conn
        self._config = config

    def search(
        self,
        query_embedding: list[float],
        *,
        top_k: int | None = None,
        exclude_superseded: bool = True,
    ) -> list[SearchResult]:
        """Find the top-k facts most similar to the query embedding.

        Args:
            query_embedding: The embedding vector of the query text.
            top_k: Number of results to return. Defaults to
                config.ask_top_k (20).
            exclude_superseded: If True, exclude facts that have been
                superseded by newer facts.

        Returns:
            A list of SearchResult, sorted by descending similarity.
        """
        raise NotImplementedError

    def has_embeddings(self) -> bool:
        """Check whether the knowledge store contains any embedded facts."""
        raise NotImplementedError
