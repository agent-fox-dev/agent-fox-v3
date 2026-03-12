# Agent Instructions

Instructions for coding agents (Cursor, Claude Code, Codex, etc.) working on
this repository. Treat this file as mandatory policy for every coding session.

## Understand Before You Code (MANDATORY)

Before making any changes, orient yourself:

1. **Read `README.md`** for project overview and quick-start.
2. **Read `docs/memory.md`** — accumulated knowledge from prior automated
   sessions: gotchas, patterns, decisions, conventions, fragile areas. Skipping
   this file means repeating mistakes that were already discovered.
3. **Read relevant specs** in `.specs/` for the area you're working on.
4. **Read ADRs** in `docs/adr/` for architectural context.
5. **Explore the codebase:** `<main_package>/` is the main package, `<test_directory>/` has
   unit, property, and integration tests.
6. **Check git state:** `git log --oneline -20`, `git status --short --branch`.
7. **Run `make check`** to confirm the baseline is green. If tests fail, fix
   them before starting new work.

**Important:** Read all documents and code in depth — don't skim.

**Important:** Only read files tracked by git. Skip anything matched by
`.gitignore`. When in doubt, run `git ls-files` to see what's tracked.

Do not implement anything before completing these steps.

## Project Structure

```
<main_package>/         # Main package
<test_directory>/       # Tests directory
docs/                   # Documentation
```

## Git Workflow

- **Branch from `develop`**, not `main`: `feature/<descriptive-name>`.
- **Never commit directly** to `main` or `develop`.
- **Conventional commits:** `<type>: <description>` (e.g. `feat:`, `fix:`,
  `refactor:`, `docs:`, `test:`, `chore:`).
- **Commit discipline:** only commit files relevant to the current change.
- **Never add `Co-Authored-By` lines.** No AI attribution in commits — ever.

## Quality Commands

Run the full quality suite before committing:

```
make check
```

## Scope Discipline

- Focus on one coherent change per session.
- Do not include unrelated "while here" fixes.
- Priority: fix broken behavior before adding new behavior.
