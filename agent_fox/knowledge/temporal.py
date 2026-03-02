"""Temporal queries: timeline construction and rendering.

Requirements: 13-REQ-4.1, 13-REQ-4.2, 13-REQ-6.1, 13-REQ-6.2, 13-REQ-6.3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import duckdb

from agent_fox.knowledge.causal import CausalFact, traverse_causal_chain
from agent_fox.knowledge.search import VectorSearch

logger = logging.getLogger("agent_fox.knowledge.temporal")


@dataclass(frozen=True)
class TimelineNode:
    """A single node in a rendered timeline."""

    fact_id: str
    content: str
    spec_name: str | None
    session_id: str | None
    commit_sha: str | None
    timestamp: str | None
    relationship: str  # "cause" | "effect" | "root"
    depth: int  # indentation level in timeline


@dataclass
class Timeline:
    """An ordered timeline of causally linked facts."""

    nodes: list[TimelineNode] = field(default_factory=list)
    query: str = ""

    def render(self, *, use_color: bool = True) -> str:
        """Render the timeline as indented text.

        Each node is rendered with indentation proportional to its depth.
        When use_color is False (stdout is not a TTY), no ANSI escape
        codes are included.
        """
        if not self.nodes:
            return ""

        lines: list[str] = []
        for node in self.nodes:
            indent = "  " * max(0, node.depth)
            if node.relationship == "effect":
                connector = "-> "
            elif node.relationship == "cause":
                connector = "<- "
            else:
                connector = "** "

            line_1 = f"{indent}{connector}{node.content}"
            commit = node.commit_sha or "n/a"
            line_2 = (
                f"{indent}   [{node.timestamp}] "
                f"spec:{node.spec_name} "
                f"session:{node.session_id} "
                f"commit:{commit}"
            )
            lines.append(line_1)
            lines.append(line_2)

        return "\n".join(lines)


def _causal_fact_to_node(fact: CausalFact) -> TimelineNode:
    """Convert a CausalFact to a TimelineNode."""
    return TimelineNode(
        fact_id=fact.fact_id,
        content=fact.content,
        spec_name=fact.spec_name,
        session_id=fact.session_id,
        commit_sha=fact.commit_sha,
        timestamp=fact.created_at,
        relationship=fact.relationship,
        depth=fact.depth,
    )


def build_timeline(
    conn: duckdb.DuckDBPyConnection,
    seed_fact_ids: list[str],
    *,
    max_depth: int = 10,
) -> Timeline:
    """Construct a timeline from seed facts by traversing the causal graph.

    1. For each seed fact, traverse the causal chain in both directions.
    2. Deduplicate facts that appear in multiple chains.
    3. Sort by timestamp, then by depth within the same timestamp.
    4. Return as a Timeline with ordered TimelineNodes.
    """
    seen_ids: set[str] = set()
    all_facts: list[CausalFact] = []

    for seed_id in seed_fact_ids:
        chain = traverse_causal_chain(
            conn, seed_id, max_depth=max_depth, direction="both"
        )
        for fact in chain:
            if fact.fact_id not in seen_ids:
                seen_ids.add(fact.fact_id)
                all_facts.append(fact)

    # Sort by timestamp ascending, then by depth as tiebreaker
    all_facts.sort(key=lambda f: (f.created_at or "", f.depth))

    nodes = [_causal_fact_to_node(f) for f in all_facts]
    return Timeline(nodes=nodes)


def temporal_query(
    conn: duckdb.DuckDBPyConnection,
    question: str,
    query_embedding: list[float],
    *,
    search: VectorSearch | None = None,
    top_k: int = 20,
    max_depth: int = 10,
) -> Timeline:
    """Execute a temporal query.

    1. Use the query embedding to find the top-k most similar facts
       via vector search (same as Fox Ball ask).
    2. From those seed facts, traverse the causal graph to build a
       timeline.
    3. Return the timeline for rendering and synthesis.
    """
    if search is None:
        # Lightweight default — config only needed for ask_top_k
        # which we override via top_k anyway.
        from agent_fox.core.config import KnowledgeConfig

        search = VectorSearch(conn, KnowledgeConfig())

    results = search.search(query_embedding, top_k=top_k)
    seed_fact_ids = [r.fact_id for r in results]

    if not seed_fact_ids:
        logger.info("No similar facts found for temporal query: %s", question)
        return Timeline(query=question)

    # Build timeline from seed facts
    timeline = build_timeline(conn, seed_fact_ids, max_depth=max_depth)
    timeline.query = question
    return timeline
