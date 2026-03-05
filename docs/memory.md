# Agent-Fox Memory

## Patterns

- Test files for events, progress display, property tests, and session runner activity callbacks can persist across coding sessions and remain valid for reuse without modification. _(spec: 18_live_progress, confidence: high)_
- Large test suites (1000+ tests) can pass completely after fixing isolated import ordering issues, indicating good test isolation and independence. _(spec: 18_live_progress, confidence: medium)_
- Task group 2 for spec 18_live_progress (event types and abbreviation) was completed in a prior session with all required implementations (ActivityEvent, TaskEvent, abbreviate_arg, format_duration) already in place. _(spec: 18_live_progress, confidence: high)_
- Task group completion should be verified against actual implementation state rather than assumed incomplete; the ProgressDisplay class was already fully implemented from a prior session with all subtasks satisfied. _(spec: 18_live_progress, confidence: high)_
- Task group completion can be verified by confirming all subtasks are implemented and passing the full test suite (1029 tests) with clean linting. _(spec: 18_live_progress, confidence: high)_
- Progress tracking implementation spans multiple components: task_callback on Orchestrator, TaskEvent emission from session result handlers, and ProgressDisplay integration in command execution. _(spec: 18_live_progress, confidence: high)_
- When implementing path abbreviation features, write both unit tests (covering specific cases) and property tests (validating general behavior patterns) to ensure comprehensive coverage of the new functionality. _(spec: 18_live_progress, confidence: high)_
- Trailing path component abbreviation requires validation against existing basename-only implementations to ensure backward compatibility and correct behavior transitions. _(spec: 18_live_progress, confidence: medium)_
- Path abbreviation algorithms should prefer trailing component preservation over simple basename extraction, keeping multiple path components when space permits and using an ellipsis prefix (…/) to indicate truncation. _(spec: 18_live_progress, confidence: high)_
- Path abbreviation with space constraints requires a fallback strategy: when trailing components don't fit within max_len even with ellipsis prefix, fall back to basename-only output. _(spec: 18_live_progress, confidence: high)_
- A comprehensive checkpoint should verify multiple validation criteria: test suite passage (1034 tests), linter compliance, and business logic properties (abbreviation idempotence). _(spec: 18_live_progress, confidence: high)_
- Idempotence is a critical property to verify for abbreviation/truncation operations to ensure repeated applications produce stable results. _(spec: 18_live_progress, confidence: high)_
- Multi-phase task completion (9 sequential groups) benefits from checkpoint verification that confirms all previous phases remain valid. _(spec: 18_live_progress, confidence: medium)_
- Git branch management utilities should include separate functions for checking local vs. remote branch existence to handle different operational contexts. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- Default branch detection should be a dedicated function rather than hardcoded, as it varies by repository configuration. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- Async branch management functions (like ensure_develop) should be properly wired through CLI initialization to maintain async/await consistency throughout the codebase. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- When removing git operations from agent prompts, audit all related documentation files (git-flow.md, coding.md, coordinator.md) to ensure consistency across the codebase. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- GitHubPlatform can be implemented using httpx with REST API instead of relying on the gh CLI tool, providing more direct control and fewer external dependencies. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- Parse GitHub remote URLs (e.g., git@github.com:owner/repo.git) into structured components using a dedicated utility function for reusability across the codebase. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- When simplifying a configuration class, systematically remove associated factory functions and null/placeholder implementations that were built around the more complex structure. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- After major structural changes to a core module (like PlatformConfig), all related test files must be reviewed and updated or removed, including factory tests, protocol tests, and property-based tests. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- Post-harvest remote integration should be wired into the session lifecycle via a static method on the session runner class, with conditional push/PR logic based on branch type and remote platform configuration. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- Remote integration logic branches on two dimensions: branch type (develop vs feature) and platform settings (auto_merge enabled/disabled), determining whether to push directly or create a pull request. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- Checkpoint validation for platform/git overhaul involves verifying 1040+ tests pass, spec tests pass, linter cleanliness, file deletion confirmation, and config simplification together as a cohesive acceptance criteria set. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- ensure_develop function should be integrated into session lifecycle rather than called ad-hoc, ensuring consistent develop branch management across the application. _(spec: 19_git_and_platform_overhaul, confidence: high)_

## Decisions

- The develop branch setup should be integrated early in the session lifecycle, specifically before worktree creation, to ensure proper initialization order. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- Git push instructions should be removed from agent prompt templates to prevent unintended repository modifications. This includes push retry logic in FAILURE POLICY sections. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- Simplifying a Platform protocol to a single responsibility method (create_pr) makes the interface more maintainable and easier to implement across different platforms. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- Spec-versioned tests (e.g., spec-10 tests) may become obsolete during major overhauls and should be identified and removed rather than patched during structural changes. _(spec: 19_git_and_platform_overhaul, confidence: medium)_
- PlatformConfig should be simplified as part of platform overhaul work, reducing configuration complexity alongside git and platform infrastructure changes. _(spec: 19_git_and_platform_overhaul, confidence: high)_

## Conventions

- Import ordering in Python test files is subject to linter checks and should be reviewed when running linting passes across a test suite. _(spec: 18_live_progress, confidence: high)_
- When verifying completed task groups, ensure all 1029 tests pass and linting is clean before marking as complete to maintain code quality standards. _(spec: 18_live_progress, confidence: high)_
- A comprehensive test suite (1029 tests passing including 14 progress display specific tests) combined with clean linting provides confidence in marking a task group as complete. _(spec: 18_live_progress, confidence: high)_
- Use test naming conventions (TS-##-#) to organize and track related tests in test suites, especially when implementing multi-faceted features like path abbreviation. _(spec: 18_live_progress, confidence: medium)_
- When refactoring core utility functions like path abbreviation, update all existing tests to match the new behavior rather than reverting to old logic, then validate against full test suite. _(spec: 18_live_progress, confidence: high)_
- Package exports should be updated when refactoring internal implementations to maintain clean public API contracts. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- Updating a module's __init__.py exports is essential after deleting or restructuring internal files to prevent broken imports and ensure the public API remains clean. _(spec: 19_git_and_platform_overhaul, confidence: high)_
- A helper function like get_remote_url() in git.py is needed to abstract remote URL retrieval for use in integration workflows. _(spec: 19_git_and_platform_overhaul, confidence: medium)_
- Supersession banners should already be present in earlier specification files (e.g., spec 10) when implementing platform overhaul work, avoiding duplicate implementation. _(spec: 19_git_and_platform_overhaul, confidence: medium)_

## Anti-Patterns

- Template code should not contain direct git push commands; push operations must be wired through proper lifecycle management (e.g., session lifecycle) instead. _(spec: 19_git_and_platform_overhaul, confidence: high)_
