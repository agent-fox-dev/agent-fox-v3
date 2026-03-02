"""CLI ask command for querying the Fox Ball knowledge oracle.

Wires up the oracle pipeline and renders the answer with sources,
contradictions, and confidence indicator.

Requirements: 12-REQ-5.1, 12-REQ-5.E1, 12-REQ-5.E2, 12-REQ-2.E2
"""

from __future__ import annotations

import click

from agent_fox.knowledge.db import open_knowledge_store  # noqa: F401
from agent_fox.knowledge.embeddings import EmbeddingGenerator  # noqa: F401
from agent_fox.knowledge.oracle import Oracle  # noqa: F401
from agent_fox.knowledge.search import VectorSearch  # noqa: F401


@click.command("ask")
@click.argument("question")
@click.option(
    "--top-k",
    type=int,
    default=None,
    help="Number of facts to retrieve (default: from config)",
)
@click.pass_context
def ask_command(ctx: click.Context, question: str, top_k: int | None) -> None:
    """Ask a question about your project's accumulated knowledge.

    Embeds the question, retrieves relevant facts from the knowledge
    store, and synthesizes a grounded answer with source citations.

    Example:
        agent-fox ask "why did we choose DuckDB over SQLite?"
    """
    raise NotImplementedError
