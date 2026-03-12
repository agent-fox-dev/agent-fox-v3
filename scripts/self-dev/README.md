# Self-Development Container

Solves the bootstrapping problem: when agent-fox works on its own codebase,
breaking changes can leave the running executor unstable. This container
isolates the **executor** (a frozen v2.2.1 install) from the **workspace**
(the live repo it edits).

## Architecture

```
┌─────────────────────────────────────────────┐
│  Podman container                           │
│                                             │
│  /opt/agent-fox-venv/   ← frozen executor   │
│    (installed from GitHub tag v2.2.1)       │
│                                             │
│  /workspace/            ← bind-mounted repo │
│    (your local checkout, read-write)        │
│                                             │
│  claude CLI              ← Claude Code      │
│  uv, git, make           ← dev tools        │
└─────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Set your API key
export ANTHROPIC_API_KEY=sk-...

# 2. Build the image (one-time, ~2 min)
cd scripts/self-dev
podman-compose build

# 3. Run agent-fox against its own repo
podman-compose run --rm agent-fox run "fix the flaky test in test_config.py"
```

## Updating the Executor Version

To pin a different version, rebuild with:

```bash
podman-compose build --build-arg AF_VERSION=v2.3.0
```

## Passing API Keys

Set environment variables in your shell before running, or create a
`scripts/self-dev/.env` file:

```env
ANTHROPIC_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
```

## How It Works

1. The Containerfile clones agent-fox at a pinned git tag and installs it
   into `/opt/agent-fox-venv` — this never changes at runtime.
2. Your local repo is bind-mounted at `/workspace` — agent-fox reads and
   writes files here, runs `make check`, etc.
3. Even if the workspace code is completely broken, the executor in
   `/opt/agent-fox-venv` keeps running because it's a separate install.
