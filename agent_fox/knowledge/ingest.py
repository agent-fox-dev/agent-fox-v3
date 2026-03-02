"""Knowledge source ingestion for the Fox Ball.

Ingests additional knowledge sources (ADRs, git commits) into the
knowledge store alongside session-extracted facts.

Requirements: 12-REQ-4.1, 12-REQ-4.2, 12-REQ-4.3
"""

from __future__ import annotations

import logging
import subprocess  # noqa: F401
from dataclasses import dataclass
from pathlib import Path

import duckdb  # noqa: F401

from agent_fox.knowledge.embeddings import EmbeddingGenerator

logger = logging.getLogger("agent_fox.knowledge.ingest")


@dataclass(frozen=True)
class IngestResult:
    """Summary of an ingestion run."""

    source_type: str  # "adr" | "git"
    facts_added: int
    facts_skipped: int  # already ingested
    embedding_failures: int


class KnowledgeIngestor:
    """Ingests additional knowledge sources into the Fox Ball.

    Parses ADRs and git commit messages, creates facts, generates
    embeddings, and stores them in DuckDB alongside session facts.
    """

    def __init__(
        self,
        conn: duckdb.DuckDBPyConnection,
        embedder: EmbeddingGenerator,
        project_root: Path,
    ) -> None:
        self._conn = conn
        self._embedder = embedder
        self._project_root = project_root

    def ingest_adrs(self, adr_dir: Path | None = None) -> IngestResult:
        """Ingest ADRs from docs/adr/ as facts.

        Each ADR markdown file is parsed into a single fact with:
        - content: the ADR title and body
        - category: "adr"
        - spec_name: the ADR filename (e.g., "001-use-duckdb.md")
        - commit_sha: None (ADRs are not tied to a specific commit)

        Skips ADRs that have already been ingested (by checking
        for existing facts with the same spec_name and category).

        Returns:
            An IngestResult summarizing what was ingested.
        """
        raise NotImplementedError

    def ingest_git_commits(
        self,
        *,
        limit: int = 100,
        since: str | None = None,
    ) -> IngestResult:
        """Ingest git commit messages as facts.

        Each commit is stored as a fact with:
        - content: the commit message (subject + body)
        - category: "git"
        - commit_sha: the commit's SHA
        - created_at: the commit's author date

        Skips commits that have already been ingested (by checking
        for existing facts with the same commit_sha and category).

        Args:
            limit: Maximum number of commits to ingest.
            since: Only ingest commits after this date (ISO 8601).

        Returns:
            An IngestResult summarizing what was ingested.
        """
        raise NotImplementedError

    def _parse_adr(self, path: Path) -> tuple[str, str]:
        """Parse an ADR markdown file into (title, body)."""
        raise NotImplementedError

    def _is_already_ingested(
        self,
        *,
        category: str,
        identifier: str,
    ) -> bool:
        """Check whether a source has already been ingested."""
        raise NotImplementedError
