# Product Requirements Document

| Field   | Value                                    |
|---------|------------------------------------------|
| Version | 1.0                                      |
| Author  | Reverse-engineered from codebase         |
| Date    | 2026-03-01                               |
| Status  | Draft                                    |

## 1. Product Overview

agent-fox is an autonomous coding-agent orchestrator for developers who use
AI coding assistants but are tired of babysitting them. The developer writes
structured specifications describing what they want built, then tells
agent-fox to execute. agent-fox reads the specs, sequences tasks so that
each one's prerequisites are completed first, and drives an AI coding agent
through each task — each running independently so that one task's problems
cannot affect another. Sessions can run one at a time or up to eight in
parallel. Progress, learnings, and cost are tracked automatically. If the
process is interrupted, it resumes from where it left off.

The product targets solo developers and small teams who want to convert a
well-defined specification into a working, version-controlled codebase with
dozens of clean, traceable commits — overnight, unattended.

## 2. Goals & Non-Goals

**Goals**

- ✅ Enable unattended, spec-driven code generation across many sessions
  without human supervision.
- ✅ Preserve institutional knowledge across sessions so the agent improves
  over time and avoids repeating mistakes.
- ✅ Provide cost and progress visibility so the developer stays in control
  of spend and scope.
- ✅ Recover gracefully from interruptions, crashes, and coding failures
  without losing completed work.
- ✅ Support parallel execution to reduce wall-clock time on large specs.
- ✅ Validate specification quality before execution to catch problems early.
- ✅ Detect and auto-fix test, lint, type-check, and build failures without
  manual triage.

**Non-Goals**

- 🚫 Real-time IDE integration — agent-fox is a batch CLI tool, not an
  ambient assistant. (Planned for v2.)
- 🚫 Goal-driven planning from natural language — the developer must provide
  structured specifications; agent-fox does not infer intent from vague
  descriptions. (Planned for v2.)
- 🚫 Multi-repository orchestration — all work happens within a single
  repository.
- 🚫 Self-hosting or SaaS — agent-fox is a local developer tool, not a
  hosted service.

## 3. User Personas

| Persona | Description | Primary Need |
|---|---|---|
| Solo Developer | An individual developer who uses AI coding assistants daily but loses hours to context-switching and manual oversight. | Run large, multi-session coding tasks overnight without supervision, then review clean commits in the morning. |
| Tech Lead | A team lead who writes specs and delegates implementation. Wants AI to handle the first pass. | Convert a product spec into a working feature branch with clean history, then review via pull requests. |
| Operator / DevOps | Someone who configures and monitors agent-fox runs, manages cost budgets, and integrates with CI/CD. | Control cost, enforce quality gates (hooks, CI checks), and monitor progress without reading code. |

## 4. User Workflows

**Workflow: First-Time Setup**

1. Developer installs agent-fox.
2. Developer runs `agent-fox init` in their project directory.
3. The system creates a configuration directory, a default configuration
   file, and initializes a long-lived development branch.
4. Developer writes specifications under a `.specs/` directory (or uses
   the `/af-spec` companion skill to generate them).
5. Outcome: The project is ready for autonomous coding.

---

**Workflow: Plan and Execute**

1. Developer runs `agent-fox plan` to build an execution plan from
   specifications.
2. The system discovers all specification folders, reads their task
   definitions and dependency declarations, and produces a sequenced
   plan where prerequisites are resolved automatically.
3. Developer reviews the plan via `agent-fox status` to see task counts,
   dependencies, and scope.
4. Developer runs `agent-fox code` (optionally requesting parallel
   execution for up to 8 concurrent sessions).
5. For each ready task, the system:
   - Creates an isolated workspace so the task cannot interfere with
     other work.
   - Launches a coding agent with task-specific context and relevant
     learnings from prior sessions.
   - Runs any configured pre- and post-session quality hooks.
   - Validates the outcome and integrates the changes.
   - Extracts learnings into a persistent knowledge base.
6. The system repeats until all tasks are complete, a cost or session
   limit is reached, or a safety guard trips.
7. Developer reviews the result: a codebase with clean, focused commits
   per task, ready for human review.
8. Outcome: A complete set of changes ready for release or further review.

---

**Workflow: Monitor Progress**

1. Developer runs `agent-fox status` during or after execution.
2. The system displays: tasks completed, in progress, pending, failed,
   and blocked; token usage and estimated cost; and a list of any
   blocked or failed tasks.
3. Developer can export this as JSON or YAML for integration with
   dashboards or scripts.
4. Outcome: Developer knows exactly where things stand without reading
   logs or code.

---

**Workflow: Daily Standup Report**

1. Developer runs `agent-fox standup` (default: last 24 hours).
2. The system produces a report showing:
   - What the agent accomplished (tasks completed, sessions run, tokens
     used, cost incurred).
   - What humans committed during the same period.
   - Files modified by both the agent and a human (potential conflicts).
   - Tasks queued and ready for the next run.
   - Total cost for the reporting period.
3. Developer can adjust the reporting window (e.g., last 7 days) and
   export to JSON, YAML, or a file.
4. Outcome: Developer has a quick daily briefing on agent and human
   activity, with early warning of file-level overlaps.

---

**Workflow: Auto-Fix Failures**

1. Developer runs `agent-fox fix` on a project with broken tests, lint
   errors, or build failures.
2. The system automatically detects available quality checks (test
   runners, linters, type checkers, build tools).
3. The system runs those checks, collects failures, and groups them by
   likely root cause.
4. For each group, the system generates a fix specification and runs a
   coding session to address it.
5. The system re-runs quality checks. If failures remain, it repeats
   (up to a configurable number of passes).
6. A summary report shows what was fixed and what remains.
7. Outcome: Many common failures are resolved automatically without
   manual triage or specification authoring.

---

**Workflow: Validate Specifications**

1. Developer runs `agent-fox lint-spec` before executing a plan.
2. The system checks all specification files for structural problems:
   missing files, oversized task groups, broken dependency references,
   untraced requirements, missing acceptance criteria.
3. Findings are reported by severity (Error, Warning, Hint) in a
   table, with optional JSON or YAML export.
4. Optionally, the developer enables AI-powered semantic analysis that
   flags vague or implementation-leaking acceptance criteria.
5. Outcome: Specification problems are caught before they waste coding
   sessions and cost.

---

**Workflow: Recovery After Interruption**

1. The system is interrupted mid-run (Ctrl+C, crash, power loss).
2. Developer re-runs `agent-fox code`.
3. The system detects the previous run's state, cleans up any orphaned
   workspaces, and resumes from the first available task.
4. Completed work is preserved; only incomplete tasks are re-run.
5. Outcome: No work is lost. The developer simply re-runs the command.

---

**Workflow: Reset Failed Tasks**

1. Some tasks have failed or become blocked after exhausting retries.
2. Developer runs `agent-fox reset` to clear all incomplete tasks back
   to a ready state, or resets a single task by specifying its identifier.
3. The system cleans up associated workspaces and branches, resets task
   status, and re-evaluates which downstream tasks are now unblocked.
4. Developer re-runs `agent-fox code` to retry.
5. Outcome: Failed tasks get a fresh start without affecting completed
   work.

## 5. Functional Requirements

**Capability Area: Project Initialization**

- [REQ-001] When the user runs the init command, the system shall create a
  project configuration directory with a default configuration file and
  initialize a long-lived development branch.
- [REQ-002] When the project is already initialized, the system shall
  preserve the existing configuration and not overwrite it.
- [REQ-003] When the project is initialized, the system shall ensure that
  the developer's repository stays clean: runtime-generated temporary files
  (workspaces, logs) are excluded from version control, while configuration,
  progress state, and knowledge-base files are tracked and persist across
  sessions.

**Capability Area: Planning**

- [REQ-010] When the user runs the plan command, the system shall discover
  all specification folders, read their task definitions, and produce a
  sequenced execution plan that respects task prerequisites.
- [REQ-011] Within a specification, the system shall sequence tasks in the
  order they are defined (task 1 before task 2, etc.). Across
  specifications, the system shall respect explicit prerequisite
  declarations written in the specification documents.
- [REQ-012] Where fast mode is enabled, the system shall exclude tasks
  marked as optional and ensure that remaining tasks still connect correctly
  (i.e., if task B depends on optional task A which depends on task C,
  task B shall depend directly on task C instead).
- [REQ-013] The user shall be able to restrict planning to a single named
  specification.
- [REQ-014] The system shall save the execution plan so that subsequent
  commands (status, code) can use it without re-planning.
- [REQ-015] The user shall be able to request a full re-analysis of
  cross-specification prerequisites, discarding any previously computed
  ordering.
- [REQ-016] The user shall be able to request a background verification
  that declared prerequisites are consistent and correct.

**Capability Area: Autonomous Coding**

- [REQ-020] When the user runs the code command, the system shall
  orchestrate coding sessions for each ready task in dependency order.
- [REQ-021] Each coding session shall run in an isolated workspace,
  ensuring that one session's changes cannot interfere with other sessions
  or with already-integrated work.
- [REQ-022] The system shall provide each coding session with task-specific
  context: the relevant specification documents, and any prior learnings
  that match the current task's topic (matched by specification name and
  task keywords).
- [REQ-023] When a coding session completes successfully, the system shall
  integrate the session's changes into the shared development line and
  update the task status.
- [REQ-024] If a conflict occurs during integration, the system shall
  automatically attempt to reconcile the changes and retry. If
  reconciliation fails, the session shall be treated as failed and subject
  to retry logic (REQ-025).
- [REQ-025] When a coding session fails, the system shall retry up to
  the configured maximum retry count (default: 2) before marking the
  task as blocked.
- [REQ-026] When a task is marked as blocked, the system shall cascade-block
  all dependent tasks.
- [REQ-027] The system shall enforce a configurable session timeout
  (default: 30 minutes). If a session exceeds this timeout, it shall be
  terminated and recorded as failed.
- [REQ-028] Where a cost limit is configured, the system shall stop
  launching new sessions when cumulative cost reaches the limit. In-flight
  sessions shall be allowed to complete.
- [REQ-029] Where a session limit is configured, the system shall stop
  after the specified number of sessions.
- [REQ-030] The system shall persist state after every session so that
  execution can resume after interruption.
- [REQ-031] When the user interrupts execution (e.g., Ctrl+C), the system
  shall save state, clean up workspaces, and print resume instructions.

**Capability Area: Parallel Execution**

- [REQ-040] Where parallel execution is requested, the system shall
  execute up to the specified number of independent tasks concurrently.
- [REQ-041] The maximum parallelism shall be capped at 8. If the user
  requests more, the system shall warn and use 8.
- [REQ-042] During parallel execution, the system shall ensure that
  concurrent sessions do not corrupt already-integrated work.
- [REQ-043] During parallel execution, the system shall ensure that each
  task is executed exactly once.

**Capability Area: Sync Barriers and Hot-Loading**

- [REQ-050] At configurable intervals (default: every 5 completed
  sessions), the system shall pause execution to: run configured
  checkpoint hooks, regenerate the human-readable knowledge summary,
  and check for new specifications added since execution began.
- [REQ-051] When new specification folders appear during execution, the
  system shall incorporate them into the task graph without requiring
  a restart.

**Capability Area: Structured Memory**

- [REQ-060] After each successful coding session, the system shall extract
  structured learnings and store them in a persistent knowledge base. The
  system recognizes six categories of learnings: gotchas (things that
  tripped up the agent), patterns (successful approaches), decisions
  (architectural choices made), conventions (project style rules),
  anti-patterns (approaches to avoid), and fragile areas (code regions
  sensitive to change).
- [REQ-061] Before each coding session, the system shall select stored
  learnings relevant to the current task — matched by specification name
  and task-related keywords — and include them in the agent's working
  context, up to a budget of 50 facts.
- [REQ-062] The user shall be able to compact the knowledge base on demand,
  which removes duplicate entries (same content) and entries that have been
  superseded by newer learnings on the same topic.
- [REQ-063] The system shall maintain a human-readable summary of
  accumulated knowledge, organized by category, that the developer can
  review at any time.

**Capability Area: Error Auto-Fix**

- [REQ-070] When the user runs the fix command, the system shall detect
  available quality checks (test runners, linters, type checkers, build
  tools) by inspecting project configuration files.
- [REQ-071] The system shall run detected quality checks, collect failures,
  and group them by likely root cause using AI-assisted semantic analysis
  (e.g., grouping related test failures that share a common cause). When
  AI grouping is unavailable, the system shall fall back to one group per
  quality-check command.
- [REQ-072] For each failure group, the system shall generate a complete
  fix specification (with requirements, design, tests, and tasks) and
  execute one or more coding sessions to resolve it.
- [REQ-073] The system shall iterate: re-run quality checks after each
  pass and repeat until all checks pass or the maximum number of passes
  is reached (default: 3).
- [REQ-074] The system shall produce a summary report showing which
  failure groups were resolved and which remain.

**Capability Area: Specification Validation**

- [REQ-080] When the user runs the lint-spec command, the system shall
  check all specification files for structural and quality problems.
- [REQ-081] The system shall report findings at three severity levels:
  Error (will break execution), Warning (likely to cause problems), and
  Hint (suggestion for improvement).
- [REQ-082] Static checks shall include: missing required specification
  files (the system expects five per specification: product requirements,
  requirements, design, test specification, and task plan); task groups
  with more than 6 subtasks (suggesting the task is too large to complete
  in one session); task groups without a verification step; requirements
  without acceptance criteria; dependency references to non-existent
  specifications or task groups; and requirements not traced to any test.
- [REQ-083] Where AI-powered analysis is enabled, the system shall
  additionally flag acceptance criteria that are vague or unmeasurable, and
  criteria that describe how the system should be built rather than what it
  should do.
- [REQ-084] The system shall exit with a non-zero code if any Error-severity
  findings are present.
- [REQ-085] The system shall support output in table (default), JSON, and
  YAML formats.

**Capability Area: Progress and Reporting**

- [REQ-090] When the user runs the status command, the system shall display
  task counts by status, token usage, estimated cost, and any blocked or
  failed tasks.
- [REQ-091] When the user runs the standup command, the system shall produce
  a report covering agent activity, human commits, file-level overlaps
  between agent and human changes, cost breakdown, and queued tasks —
  within a configurable time window (default: 24 hours).
- [REQ-092] Both status and standup commands shall support JSON and YAML
  output formats.

**Capability Area: State Reset**

- [REQ-100] When the user runs the reset command without specifying a task,
  the system shall reset all incomplete tasks to a ready state, remove
  associated workspaces and branches, and prompt for confirmation before
  proceeding.
- [REQ-101] When the user specifies a single task to reset, the system
  shall reset only that task and re-evaluate whether downstream tasks
  that were previously blocked can now proceed.
- [REQ-102] The user shall be able to skip the confirmation prompt when
  performing a full reset.

**Capability Area: Hooks and Extensibility**

- [REQ-110] The system shall support configurable pre-session and
  post-session hook scripts that run in the workspace context.
- [REQ-111] The system shall support sync-barrier hook scripts that run
  at periodic intervals during execution.
- [REQ-112] Each hook may be configured in "abort" mode (failure stops
  execution) or "warn" mode (failure is logged but execution continues).
- [REQ-113] Hook scripts shall have access to context about the current
  task, including the specification name, task group number, workspace
  location, and branch name.
- [REQ-114] The user shall be able to bypass all hooks for a given run.

**Capability Area: Platform Integration**

- [REQ-120] Where the platform is configured as GitHub, the system shall
  create pull requests instead of directly merging to the development
  branch.
- [REQ-121] Pull request granularity shall be configurable: one PR per
  task group or one PR per specification.
- [REQ-122] Where CI waiting is enabled, the system shall wait for CI
  checks to pass before marking a task complete (with a configurable
  timeout, default: 10 minutes).
- [REQ-123] Where review waiting is enabled, the system shall wait for
  PR approval before proceeding.
- [REQ-124] Where auto-merge is enabled, the system shall merge the PR
  automatically when all configured gates pass.
- [REQ-125] When no platform is configured (default), the system shall
  merge directly to the development branch without creating pull requests.

**Capability Area: Security**

- [REQ-130] The system shall restrict which shell commands the coding agent
  is permitted to execute, using a configurable allowlist. Commands not on
  the list shall be blocked.
- [REQ-131] The default allowlist shall permit standard development
  operations: version control, package management, build tools, and file
  utilities (approximately 35 commands). The operator may replace this list
  entirely or extend it with additional commands via configuration.

## 6. Configuration & Input Specification

| Option | Description | Default | Valid Values |
|---|---|---|---|
| Parallelism | Maximum number of concurrent coding sessions. | 1 (sequential) | 1–8 |
| Sync interval | Number of completed sessions between sync barriers. 0 disables. | 5 | 0 or any positive integer |
| Hot-loading | Whether new specs are detected and incorporated during execution. | Enabled | Enabled / Disabled |
| Coding model | AI model used for coding sessions. | Most capable available model | Any supported model identifier |
| Coordinator model | AI model used for planning and dependency analysis. | Mid-tier model (balances cost and capability) | Any supported model identifier |
| Memory extraction model | AI model used for extracting learnings after sessions. | Lightweight model (optimizes for cost) | Any supported model identifier |
| Max retries | Maximum retry attempts per failed task. | 2 | Any non-negative integer |
| Session timeout | Maximum duration per coding session. | 30 minutes | Any positive integer (minutes) |
| Inter-session delay | Pause between sequential sessions to avoid rate limiting. | 3 seconds | Any non-negative integer (seconds) |
| Max cost | Cost ceiling that stops execution. | Unlimited | Any positive dollar amount |
| Max sessions | Session count ceiling that stops execution. | Unlimited | Any positive integer |
| Hook timeout | Maximum duration per hook script. | 300 seconds | Any positive integer (seconds) |
| Hook mode | Per-hook failure behavior. | abort | abort, warn |
| Platform type | Forge integration for PR-based workflows. | none | none, github |
| PR granularity | How pull requests are scoped. | Per task group | Per task group, Per specification |
| Wait for CI | Whether to wait for CI checks before proceeding. | Disabled | Enabled / Disabled |
| Wait for review | Whether to wait for PR approval before proceeding. | Disabled | Enabled / Disabled |
| Auto-merge | Whether to auto-merge PRs when gates pass. | Disabled | Enabled / Disabled |
| CI timeout | How long to wait for CI checks. | 600 seconds | Any positive integer (seconds) |
| PR labels | Additional labels applied to every PR. | None | List of strings |
| Command allowlist | Shell commands the coding agent may execute. | Standard development tools (~35 commands) | List of command names |
| Command allowlist (extend) | Additional commands appended to the default allowlist. | None | List of command names |
| Theme: playful mode | Use personality-flavored messages in output. | Enabled | Enabled / Disabled |
| Theme: colors | Color scheme for terminal output (header, success, error, warning, info, etc.). | Fox-themed warm palette | Any valid terminal color or style |

Configuration is stored in a project-level configuration file. Command-line
options override configuration file values where both are available.

## 7. Output Specification

**Coding Output**

- A series of focused, traceable commits — one per completed task — integrated
  into a shared development line.
- When GitHub integration is enabled: pull requests created per task group
  (or per specification, configurable), ready for team review.

**Progress State**

- The system maintains a persistent record of all progress: which tasks are
  complete, in progress, failed, or blocked; session history including
  timestamps, outcomes, token usage, cost, and duration. This record is
  updated after every session and is what enables seamless resume after
  interruption.

**Knowledge Base**

- A persistent, growing collection of project-specific learnings accumulated
  across sessions. Learnings are categorized (gotchas, patterns, decisions,
  conventions, anti-patterns, fragile areas) and include a confidence level
  and source attribution.
- A human-readable summary organized by category is maintained so the
  developer can review what the agent has learned.

**Status Output**

- Task progress: counts by status (pending, in progress, completed,
  failed, blocked, skipped).
- Token usage: total input and output tokens across all sessions.
- Estimated cost.
- Per-specification breakdown.
- Blocked and failed task list.
- Available as table, JSON, or YAML.

**Standup Report**

- Agent activity: tasks completed, sessions run, tokens consumed, cost.
- Human activity: non-agent commits in the same period.
- File overlap warnings: files modified by both agent and human.
- Queue summary: tasks ready, pending, blocked.
- Cost breakdown by model.
- Available as table, JSON, or YAML, or written to file.

**Fix Report**

- Passes completed.
- Failure clusters resolved and remaining.
- Total sessions consumed.
- Termination reason (all fixed / max passes / interrupted / cost limit).

**Lint Report**

- Findings grouped by specification, file, and rule.
- Severity levels: Error, Warning, Hint.
- Summary counts by severity.
- Available as table, JSON, or YAML.

**Audit Log (optional)**

- When debug mode is enabled, a detailed log is written per run that
  enables full reconstruction of what the agent saw, decided, and did.
  Useful for diagnosing unexpected behavior or auditing agent decisions.

## 8. Error Handling & User Feedback

**Session Failure**

- When a coding session fails, the system retries automatically (up to
  the configured limit, default: 2). On retry, the agent receives the
  previous error so it can avoid repeating the mistake.
- When retries are exhausted, the task is marked as blocked and all
  downstream tasks are cascade-blocked. The user sees which tasks are
  blocked and why in the status output.

**Integration Conflict**

- When integrating a completed session's changes causes a conflict with
  other recently integrated work, the system automatically attempts to
  reconcile the changes and retries. If reconciliation fails, the session
  is treated as a failure and subject to retry logic.

**Cost and Session Limits**

- When cumulative cost reaches the configured ceiling, the system stops
  launching new sessions, allows in-flight sessions to complete, reports
  progress, and exits. The user can resume with a higher limit.
- Session limits behave identically.

**Hook Failures**

- In "abort" mode: a failing hook stops execution immediately with a clear
  error message identifying which hook failed.
- In "warn" mode: a failing hook is logged but execution continues.

**Timeout**

- When a coding session exceeds the timeout, it is terminated and recorded
  as failed. Partial metrics (tokens, turns) are preserved.

**Interruption (Ctrl+C)**

- The system saves state, cleans up workspaces, and prints resume
  instructions. In parallel mode, in-flight sessions are cancelled.

**Stalled Progress**

- If no tasks can proceed but work remains (due to dependency cycles or all
  remaining tasks being blocked by failures), the system warns the user
  with details about which tasks are stuck and why, then exits.

**Invalid Configuration**

- Unrecognized platform types or PR granularity values produce a clear
  error and prevent execution.
- Out-of-range numeric values are clamped to valid bounds with a warning.
- Deprecated configuration keys are silently ignored with a log warning.

**No Quality Checks Found (Fix Command)**

- If the fix command cannot detect any quality-check tools in the project,
  it reports an error and exits rather than proceeding blindly.

## 9. Constraints & Assumptions

**Constraints**

- Runs on macOS and Linux. Requires a modern Python runtime (3.12+) and
  Git (2.15+) to be installed.
- Requires valid AI provider credentials configured in the environment.
- All work happens within a single Git repository.
- Maximum 8 concurrent coding sessions.

**Assumptions**

- The developer provides well-structured specifications before running
  the plan or code commands. The system does not generate specifications
  from vague descriptions (a companion skill assists with spec authoring
  but is not part of the core product).
- The target repository is in a clean state before execution begins (no
  uncommitted changes).
- A shared development line can be created or already exists as the
  integration target.
- When GitHub integration is enabled, a valid access token with appropriate
  permissions is available in the environment.

## 10. Open Questions

| # | Question | Why it matters |
|---|---|---|
| 1 | How should the system handle specifications that are modified by a human _during_ an active run? Hot-loading adds new specs, but behavior for edited existing specs mid-run is unclear. | Could lead to inconsistent state if a spec's tasks change while sessions are in flight. |
| 2 | What is the intended behavior when the development branch is force-pushed or rebased externally during a run? | Workspace isolation depends on the development branch as a stable integration target. External changes could break merges. |
| 3 | The memory compaction step (deduplication and pruning of superseded facts) appears to require manual invocation. Should it run automatically at a certain knowledge-base size? | Without automatic compaction, the knowledge base could grow unboundedly over many runs. |
| 4 | The standup report's file-overlap detection compares agent and human changes to the same files. What action, if any, should the system recommend when overlaps are detected? | Currently informational only. Users may expect guidance on resolution. |
| 5 | The platform integration supports GitHub. Are GitLab and Gitea planned, and should the PRD account for forge-neutral requirements? | The configuration accepts only "github" or "none" today. Other forges would need similar PR, CI, and review gate support. |

## 11. Future Considerations

Based on patterns in the codebase and documentation, several capabilities
appear to be planned or partially explored:

- **Knowledge Oracle:** A queryable interface that lets developers ask
  natural-language questions and receive answers grounded in the project's
  accumulated knowledge base.
- **Goal-Driven Planning:** Accepting high-level goals or GitHub issues as
  input and automatically generating specifications, rather than requiring
  hand-authored specs.
- **Multi-Archetype Agents:** Specialized agent roles beyond "coder" — such
  as a reviewer, tester, or architect — each with different prompts and
  evaluation criteria.
- **Pre-Execution Simulation:** A dry-run mode that previews what the agent
  would do before committing real resources.
- **Autonomous Overnight Maintenance:** Scheduled, cron-like execution for
  ongoing maintenance tasks (dependency updates, security patches,
  performance monitoring).
- **IDE Companion Mode:** Ambient integration with development environments,
  providing real-time suggestions and background execution.
- **Real-Time Dashboard:** A web-based interface for monitoring active runs,
  reviewing progress, and managing the knowledge base visually.
