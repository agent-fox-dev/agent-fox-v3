"""CLI command for status report: agent-fox status.

Displays a progress dashboard showing task counts, token usage,
cost, and problem tasks.

Requirements: 07-REQ-1.1, 07-REQ-1.2, 07-REQ-1.3, 07-REQ-3.1,
              23-REQ-3.1, 23-REQ-8.1, 43-REQ-1.4
"""

from __future__ import annotations

import logging
from dataclasses import asdict
from pathlib import Path

import click
from rich.console import Console

from agent_fox.cli import handle_agent_fox_errors
from agent_fox.reporting.formatters import (
    OutputFormat,
    get_formatter,
    write_output,
)
from agent_fox.reporting.status import generate_status

logger = logging.getLogger(__name__)

_AGENT_FOX_DIR = ".agent-fox"
_DEFAULT_DB_PATH = Path(".agent-fox/knowledge.db")


def _get_model_conn():
    """Open a read-only DuckDB connection for project model queries.

    Returns None if the database does not exist.

    Requirement: 43-REQ-1.4
    """
    try:
        import duckdb

        if not _DEFAULT_DB_PATH.exists():
            return None
        return duckdb.connect(str(_DEFAULT_DB_PATH), read_only=True)
    except Exception:
        logger.warning("Failed to open DuckDB for project model", exc_info=True)
        return None


@click.command("status")
@click.option(
    "--model", is_flag=True, default=False, help="Include project model."
)
@click.pass_context
@handle_agent_fox_errors
def status_cmd(ctx: click.Context, model: bool) -> None:
    """Show execution progress dashboard."""
    json_mode = ctx.obj.get("json", False)
    project_root = Path.cwd()
    agent_dir = project_root / _AGENT_FOX_DIR
    state_path = agent_dir / "state.jsonl"
    plan_path = agent_dir / "plan.json"

    report = generate_status(state_path, plan_path)

    if json_mode:
        from agent_fox.cli.json_io import emit

        emit(asdict(report))
    else:
        console = Console()
        formatter = get_formatter(OutputFormat.TABLE, console=console)
        content = formatter.format_status(report)
        write_output(content, console=console)

    # Append project model output when --model is requested
    if model:
        conn = _get_model_conn()
        if conn is not None:
            try:
                from agent_fox.knowledge.project_model import (
                    build_project_model,
                    format_project_model,
                )

                pm = build_project_model(conn)
                output = format_project_model(pm)
                if json_mode:
                    from agent_fox.cli.json_io import emit

                    emit({"project_model": asdict(pm)})
                else:
                    console = Console()
                    console.print()
                    console.print(output)
            finally:
                conn.close()
        else:
            logger.info("No DuckDB database found; skipping project model output")
