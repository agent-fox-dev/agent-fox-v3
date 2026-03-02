# agent-fox

```
   /\_/\  __
  / o.o \/  \
 ( > ^ < )   )
  \_^_/\_/--'
```

**Point agent-fox at a spec. Walk away. Come back to working code across 50+
commits.**

agent-fox is an autonomous coding-agent orchestrator. It reads your
specifications, builds a dependency graph of tasks, and drives a Claude coding
agent through each one — in isolated git worktrees, with fresh context windows,
no human intervention needed. Run tasks sequentially or up to 8 in parallel.

## Before agent-fox

You write a spec, then sit in front of your terminal babysitting an AI agent
for hours. You paste context, fix merge conflicts, restart after crashes, and
lose track of what's done. By session 10 you're exhausted and the agent has
forgotten everything from session 1.

## With agent-fox

You write the same spec, run `agent-fox code`, and go do something else. The
fox reads your specs, plans the work, spins up isolated worktrees, runs each
session with the right context, handles merge conflicts, retries failures,
extracts learnings into structured memory, and merges clean commits to
`develop`. You come back to a finished feature branch and a standup report.

## Development

```bash
uv sync --group dev
make test              # all tests
make lint              # check lint + formatting
make check             # lint + all tests
```