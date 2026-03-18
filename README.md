# agent-fox

<p align="center">
    <picture>
        <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/agent-fox-dev/agent-fox/refs/heads/main/docs/assets/agent-fox-mascot.png">
        <img src="https://raw.githubusercontent.com/agent-fox-dev/agent-fox/refs/heads/main/docs/assets/agent-fox-mascot.png" width="200">
    </picture>
</p>

**Point agent-fox at a spec. Walk away. Come back to working code across 50+
commits.**

agent-fox is an autonomous coding-agent orchestrator. It reads your
specifications, builds a dependency graph of tasks, and drives
Claude coding agents through each one — in parallel, in isolated worktrees,
with structured memory, adaptive model routing, and multi-archetype review
pipelines.

## Installation

```bash
uv tool install agent-fox
```

## Quick Start

```bash
# Initialize your project (use --skills to install Claude Code skills)
agent-fox init --skills

# Create the task graph from your specs
agent-fox plan

# Run autonomous coding sessions with 4 agents in parallel
agent-fox code --parallel 4

# Check progress
agent-fox status
```

## Documentation

Full documentation lives in [`docs/`](docs/README.md):

- [CLI Reference](docs/cli-reference.md) — all commands, flags, and exit codes
- [Configuration](docs/configuration.md) — every `config.toml` option
- [Archetypes](docs/archetypes.md) — agent roles (Coder, Skeptic, Oracle, Auditor, Verifier, …)
- [Skills](docs/skills.md) — bundled Claude Code slash commands (`/af-spec`, `/af-fix`, …)

## Development

```bash
uv sync --group dev
make check             # lint + all tests
```
