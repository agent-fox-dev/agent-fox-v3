"""CLI entry point for agent-fox.

Stub: defines Click group signature only.
Full implementation in task group 4.
"""

from __future__ import annotations

import click

from agent_fox import __version__


@click.group()
@click.version_option(version=__version__)
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging")
@click.option("--quiet", "-q", is_flag=True, help="Suppress info messages")
@click.pass_context
def main(ctx: click.Context, verbose: bool, quiet: bool) -> None:
    """agent-fox: autonomous coding-agent orchestrator."""
    ctx.ensure_object(dict)
