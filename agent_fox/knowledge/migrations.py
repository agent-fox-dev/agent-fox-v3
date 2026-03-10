"""Schema version table, forward-only migration runner, migration registry.

Requirements: 11-REQ-3.1, 11-REQ-3.2, 11-REQ-3.3, 11-REQ-3.E1,
              27-REQ-1.1, 27-REQ-1.2, 27-REQ-2.1, 27-REQ-2.2
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass

import duckdb  # noqa: F401

from agent_fox.core.errors import KnowledgeStoreError  # noqa: F401

logger = logging.getLogger("agent_fox.knowledge.migrations")

MigrationFn = Callable[[duckdb.DuckDBPyConnection], None]


@dataclass(frozen=True)
class Migration:
    """A forward-only schema migration."""

    version: int
    description: str
    apply: MigrationFn


def _migrate_v2(conn: duckdb.DuckDBPyConnection) -> None:
    """Add review_findings and verification_results tables.

    Requirements: 27-REQ-1.1, 27-REQ-1.2, 27-REQ-2.1, 27-REQ-2.2
    """
    conn.execute("""
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

        CREATE TABLE IF NOT EXISTS verification_results (
            id              UUID PRIMARY KEY,
            requirement_id  TEXT NOT NULL,
            verdict         TEXT NOT NULL,
            evidence        TEXT,
            spec_name       TEXT NOT NULL,
            task_group      TEXT NOT NULL,
            session_id      TEXT NOT NULL,
            superseded_by   TEXT,
            created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)


# Registry of all migrations, ordered by version.
MIGRATIONS: list[Migration] = [
    Migration(
        version=2,
        description="add review_findings and verification_results tables",
        apply=_migrate_v2,
    ),
]


def get_current_version(conn: duckdb.DuckDBPyConnection) -> int:
    """Return the current schema version, or 0 if no version table."""
    try:
        result = conn.execute("SELECT MAX(version) FROM schema_version").fetchone()
    except duckdb.CatalogException:
        # schema_version table does not exist yet
        return 0
    if result is None or result[0] is None:
        return 0
    return int(result[0])


def apply_pending_migrations(conn: duckdb.DuckDBPyConnection) -> None:
    """Apply all migrations newer than the current schema version.

    Each migration runs in its own transaction. On failure, raises
    KnowledgeStoreError with the failing version and cause.
    """
    current = get_current_version(conn)

    for migration in MIGRATIONS:
        if migration.version <= current:
            continue
        try:
            migration.apply(conn)
            record_version(conn, migration.version, migration.description)
            logger.info(
                "Applied migration v%d: %s",
                migration.version,
                migration.description,
            )
        except KnowledgeStoreError:
            raise
        except Exception as exc:
            raise KnowledgeStoreError(
                f"Migration to version {migration.version} failed: {exc}",
                version=migration.version,
            ) from exc


def record_version(
    conn: duckdb.DuckDBPyConnection,
    version: int,
    description: str,
) -> None:
    """Insert a row into schema_version."""
    conn.execute(
        "INSERT INTO schema_version (version, description) VALUES (?, ?)",
        [version, description],
    )
