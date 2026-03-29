# PRD: Knowledge Feedback Loop & Quality Gate Hardening

> Source: post-run analysis of parking-fee-service knowledge.duckdb
> (2026-03-17 runs). All 27 sessions completed but the knowledge graph,
> review pipeline, and complexity calibration were effectively inert.

## Problem Statement

After a full agent-fox run across 9 specs (27 sessions, $14.99), the
knowledge.duckdb contains zero session-derived facts, zero review findings,
zero verification verdicts, zero drift findings, and zero causal links. The
only populated knowledge is 100 git-commit facts ingested verbatim — a mirror
of `git log` that adds no value over the log itself.

This means:

1. **No learning between sessions.** Session N cannot benefit from gotchas
   discovered in session N-1 because fact extraction never ran.
2. **No quality signal.** Skeptic, Verifier, and Oracle archetypes were
   enabled in config but produced no records, so there is no evidence that
   generated code satisfies the specs.
3. **No post-session validation.** A session is marked "completed" when the
   coder finishes, not when the project's quality gate (`make check`) passes.
   A green coder session can produce code that fails lint or tests.
4. **No complexity calibration.** All 27 tasks were predicted STANDARD and
   landed STANDARD, yet wall-clock duration varied 5x (118 s to 599 s). The
   feature vector lacks signals that would discriminate these tasks.
5. **No causal graph.** The `fact_causes` table is empty, so pattern detection
   and temporal queries return nothing.

## Goals

1. **Session-derived facts flow into the knowledge graph** after every
   successful coder session, with embeddings and causal links.
2. **Review archetypes produce persistent records** — Skeptic findings,
   Verifier verdicts, and Oracle drift findings are stored in DuckDB and
   surfaced in subsequent sessions.
3. **A project quality gate runs after each coder session** and its
   pass/fail result is recorded as an execution signal.
4. **Complexity prediction uses richer signals** so predicted tier better
   correlates with actual cost and duration.
5. **A dedicated review-only run mode** allows a post-implementation sweep
   without re-running coder sessions.
6. **Causal links are extracted** when new facts are stored, populating the
   `fact_causes` table for pattern detection.

## Non-Goals

- Changing the archetype prompt templates (Skeptic, Verifier, Oracle).
- Adding new archetypes.
- Modifying the DuckDB schema (all required tables already exist).
- Changing the embedding model or vector dimensions.
- Implementing a UI or dashboard for knowledge exploration.

---

## 1. Session Fact Extraction (Knowledge Harvest)

### Current State

`extract_and_store_knowledge()` in `engine/knowledge_harvest.py` is called
only when a session summary artifact exists (`_read_session_artifacts`). If the
coder session does not write a summary file, extraction silently skips. The
parking-fee-service run produced zero session-derived facts, indicating
summaries were either not written or not found.

### Requirements

| ID | Requirement |
|----|-------------|
| KFL-1.1 | When a coder session completes successfully, the engine SHALL call `extract_and_store_knowledge` with the full session transcript (not just the summary artifact). If the summary artifact is missing, the transcript itself SHALL be used as fallback input. |
| KFL-1.2 | Extracted facts SHALL be inserted into `memory_facts` with category, confidence, spec_name, session_id, and commit_sha populated. |
| KFL-1.3 | Embeddings SHALL be generated for every newly inserted fact and stored in `memory_embeddings`. Embedding failures SHALL be logged but SHALL NOT block fact storage. |
| KFL-1.4 | After fact insertion, the engine SHALL call `_extract_causal_links()` to populate the `fact_causes` table with relationships between the new facts and all prior non-superseded facts. |
| KFL-1.5 | A `harvest.complete` audit event SHALL be emitted after successful extraction, including the count of facts extracted, categories present, and count of causal links created. |
| KFL-1.6 | If extraction produces zero facts from a non-trivial transcript (> 500 tokens), a warning-severity audit event SHALL be emitted to flag potential extraction prompt degradation. |

### Key Decisions

- **Transcript over summary.** The summary artifact is a lossy compression.
  Feeding the full transcript to the extraction LLM yields richer facts
  (gotchas, anti-patterns, fragile areas) that a summary omits.
- **Causal extraction on every harvest.** Running causal link extraction after
  every session is more expensive but ensures the graph stays connected. The
  alternative (batch extraction) risks stale links and complicates
  incremental queries.

---

## 2. Review Archetype Record Persistence

### Current State

Skeptic, Verifier, and Oracle are enabled in config (`config.toml`) and the
archetype injection code adds them to the task graph. However, the
parking-fee-service run shows zero rows in `review_findings`,
`verification_results`, and `drift_findings`. Either the archetype sessions
did not run, their output was not parsed, or parsed output was not persisted.

### Requirements

| ID | Requirement |
|----|-------------|
| KFL-2.1 | When a Skeptic session completes, the engine SHALL parse its structured JSON output and call `insert_review_finding()` for each finding. Findings SHALL be stored in `review_findings` with severity, description, requirement_ref, spec_name, task_group, and session_id. |
| KFL-2.2 | When a Verifier session completes, the engine SHALL parse its structured JSON output and call `insert_verification_result()` for each verdict. Verdicts SHALL be stored in `verification_results` with requirement_id, verdict (PASS/FAIL/PARTIAL), evidence, spec_name, task_group, and session_id. |
| KFL-2.3 | When an Oracle session completes, the engine SHALL parse its structured JSON output and store each drift finding in `drift_findings` with severity, description, spec_ref, artifact_ref, spec_name, task_group, and session_id. |
| KFL-2.4 | Supersession logic SHALL apply: when a new finding/verdict is inserted for the same spec_name + requirement_ref (or requirement_id), prior rows SHALL have their `superseded_by` column set to the new row's id. |
| KFL-2.5 | If an archetype session completes but produces no parseable structured output, a warning-severity audit event SHALL be emitted with the raw output truncated to 2000 characters for diagnosis. |
| KFL-2.6 | Review findings and verification verdicts SHALL be queryable by downstream sessions — the context assembly step SHALL include non-superseded critical/major findings for the current spec in the coder prompt when a retry is triggered. |

### Key Decisions

- **Parse failures are warnings, not errors.** A malformed Skeptic response
  should not block the run. Log and continue.
- **Supersession by spec + ref.** This ensures the latest verdict for each
  requirement is always the active one, regardless of how many review passes
  have run.

---

## 3. Post-Session Quality Gate

### Current State

The `post_code` hook in config is empty. A coder session is marked
"completed" based on the coder's self-assessment, with no external validation.
The project defines `make check` (lint + tests) as its quality gate.

### Requirements

| ID | Requirement |
|----|-------------|
| KFL-3.1 | The engine SHALL support a `quality_gate` configuration field (string, shell command) in `[orchestrator]`. When set, the command is executed after every successful coder session, in the project root, with a configurable timeout (default: 300 s). |
| KFL-3.2 | The quality gate result (exit code, stdout tail, stderr tail, duration_ms) SHALL be recorded in `execution_outcomes` as additional fields or in `audit_events` as a `quality_gate.result` event with pass/fail status. |
| KFL-3.3 | If the quality gate fails (non-zero exit), the session status SHALL be downgraded from "completed" to "completed_with_gate_failure". This status SHALL be visible in `session_outcomes` and `execution_outcomes`. |
| KFL-3.4 | A quality gate failure SHALL NOT block subsequent sessions. It is a signal, not a hard gate. The Verifier and Skeptic archetypes provide the blocking mechanism. |
| KFL-3.5 | When `quality_gate` is not configured, behavior SHALL be unchanged from the current implementation. |

### Key Decisions

- **Signal, not gate.** Blocking the entire run on a test failure is too
  aggressive — a flaky test in spec 03 should not prevent spec 04 from
  starting. The quality gate records the result; the Verifier archetype
  decides whether to block.
- **Shell command, not hardcoded.** Different projects use different commands
  (`make check`, `cargo test`, `pytest`). A configurable string is the
  simplest universal interface.

---

## 4. Complexity Feature Vector Enrichment

### Current State

The feature vector (`routing/features.py`) contains five signals:
`subtask_count`, `spec_word_count`, `has_property_tests`, `edge_case_count`,
`dependency_count`. All 27 tasks in the parking-fee-service run were predicted
STANDARD with 0.6 confidence, despite wall-clock durations ranging from 118 s
to 1353 s.

### Requirements

| ID | Requirement |
|----|-------------|
| KFL-4.1 | The feature vector SHALL be extended with `file_count_estimate`: the number of files expected to be created or modified, derived from the task description in `tasks.md` (count of file paths mentioned). |
| KFL-4.2 | The feature vector SHALL be extended with `cross_service_integration`: a boolean indicating whether the task group's description references services outside the current spec (detected by presence of other spec names or service names in the task text). |
| KFL-4.3 | The feature vector SHALL be extended with `language_set`: the set of programming languages involved in the task group (derived from file extensions in `tasks.md` or the spec's tech stack section). Encoded as a frozenset for hashing, serialized as a sorted list in JSON. |
| KFL-4.4 | The feature vector SHALL be extended with `historical_mean_duration_ms`: the mean duration of completed execution outcomes for the same spec, or None if no prior outcomes exist. This enables the statistical assessor to learn from same-spec history. |
| KFL-4.5 | The heuristic assessor thresholds SHALL be updated to incorporate the new signals. Specifically: tasks with `cross_service_integration=True` or `file_count_estimate >= 8` SHALL be assessed as ADVANCED (confidence 0.7) unless overridden by the statistical model. |
| KFL-4.6 | All new feature vector fields SHALL be included in the `feature_vector` JSON column of `complexity_assessments` for reproducibility and future model training. |

### Key Decisions

- **File count from task text, not filesystem.** At assessment time the files
  may not exist yet. Counting path mentions in `tasks.md` is a reasonable
  proxy.
- **Language set, not single language.** A task that touches both Go and
  protobuf (e.g., spec 08) is meaningfully more complex than a pure-Go task.
- **Historical duration as a feature.** This gives the statistical assessor a
  regression target that directly correlates with cost.

---

## 5. Review-Only Run Mode

### Current State

A run always executes the full task graph including coder sessions. There is no
way to run only the review/verification archetypes against already-implemented
code. The second parking-fee-service run (20260317_180333) was a no-op — it
found no coder work to do and exited in < 1 second, without running any
review archetypes.

### Requirements

| ID | Requirement |
|----|-------------|
| KFL-5.1 | The CLI SHALL accept a `--review-only` flag (or equivalent configuration key `review_only = true`). When set, the engine SHALL skip all coder sessions and execute only the enabled review archetypes (Skeptic, Verifier, Oracle) against the current codebase state. |
| KFL-5.2 | In review-only mode, the task graph SHALL be constructed with only review archetype nodes. Skeptic and Oracle nodes SHALL be created for each spec that has implementation artifacts. Verifier nodes SHALL be created for each spec that has a `requirements.md`. |
| KFL-5.3 | Review-only mode SHALL populate `review_findings`, `verification_results`, and `drift_findings` following the same persistence rules as KFL-2.x. |
| KFL-5.4 | Review-only mode SHALL emit `run.start` and `run.complete` audit events with a `mode: "review_only"` field in the payload. |
| KFL-5.5 | Review-only mode SHALL NOT modify any source files. All archetype sessions SHALL run with write access disabled (read-only workspace). |
| KFL-5.6 | At run completion, a summary SHALL be printed listing: total findings by severity, total verdicts by status (PASS/FAIL/PARTIAL), and total drift findings by severity. |

### Key Decisions

- **Spec-level granularity.** Each spec gets its own Skeptic/Verifier/Oracle
  session. This matches the existing per-spec session model and allows
  parallel execution.
- **Read-only enforcement.** Review archetypes should never modify code.
  Enforcing this at the workspace level (not just the prompt) prevents
  accidental writes.
- **Reuses existing archetype logic.** No new archetype code — just a
  different graph construction that omits coder nodes.

---

## 6. Causal Link Population

### Current State

The `_extract_causal_links()` function exists in `knowledge_harvest.py` and is
called after fact extraction. The `fact_causes` table exists with the correct
schema. Yet it contains zero rows after the parking-fee-service run, implying
the function either was not reached (because fact extraction itself did not
run) or returned empty results.

### Requirements

| ID | Requirement |
|----|-------------|
| KFL-6.1 | Causal link extraction SHALL be triggered after every successful fact extraction that produces >= 1 new fact, as specified in KFL-1.4. |
| KFL-6.2 | The causal extraction prompt SHALL include all non-superseded facts (not just facts from the current session) to enable cross-session causal discovery. If the total fact count exceeds the context window, facts SHALL be ranked by embedding similarity to the new facts and the top N (configurable, default 200) SHALL be included. |
| KFL-6.3 | Extracted causal links SHALL be stored in `fact_causes` with `INSERT OR IGNORE` semantics (idempotent). |
| KFL-6.4 | A `fact.causal_links` audit event SHALL be emitted after link extraction, including the count of new links created and total links in the graph. |
| KFL-6.5 | The `traverse_causal_chain()` query function SHALL be exercised by the Oracle archetype when constructing context for drift detection. The Oracle prompt SHALL include causally-related facts for each spec under review. |
| KFL-6.6 | When the fact count is < 5, causal link extraction SHALL be skipped (insufficient data for meaningful relationships). A debug-level log message SHALL note the skip. |

### Key Decisions

- **Minimum fact threshold.** Causal extraction with < 5 facts produces noise.
  Skipping it saves an LLM call per early session.
- **Similarity-ranked context window.** Loading all facts into the causal
  extraction prompt does not scale. Ranking by embedding similarity to new
  facts ensures the most relevant prior facts are included.

---

## Dependencies

| ID | Depends On | Relationship |
|----|-----------|--------------|
| KFL-1.x | None | Standalone — fixes the harvest pipeline |
| KFL-2.x | None | Standalone — fixes archetype output persistence |
| KFL-3.x | None | Standalone — adds quality gate |
| KFL-4.x | None | Standalone — enriches feature vector |
| KFL-5.x | KFL-2.x | Review-only mode requires archetype persistence to be working |
| KFL-6.x | KFL-1.x | Causal links require facts to exist |

## Out of Scope

- Changing Skeptic/Verifier/Oracle prompt templates or output schemas.
- Adding new DuckDB tables or modifying existing schemas.
- Building a visualization layer or dashboard.
- Implementing fact compaction or garbage collection.
- Tuning embedding models or dimensions.
- Adding new archetypes.
- Modifying the git workflow or branching strategy.
