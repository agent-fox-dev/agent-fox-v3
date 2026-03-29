"""Spec analysis helpers shared by the graph builder and injection modules.

Extracted to break the circular dependency between builder.py and injection.py.

Requirements: 46-REQ-3.1, 46-REQ-3.2, 46-REQ-4.4
"""

from __future__ import annotations

import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Test-writing group detection (46-REQ-3.1, 46-REQ-3.2)
# ---------------------------------------------------------------------------

_TEST_GROUP_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"write failing spec tests", re.IGNORECASE),
    re.compile(r"write failing tests", re.IGNORECASE),
    re.compile(r"create unit test", re.IGNORECASE),
    re.compile(r"create test file", re.IGNORECASE),
    re.compile(r"spec tests", re.IGNORECASE),
]


def is_test_writing_group(title: str) -> bool:
    """Return True if the group title matches a test-writing pattern.

    Requirements: 46-REQ-3.1, 46-REQ-3.2, 46-REQ-3.E1, 46-REQ-3.E2
    """
    return any(p.search(title) for p in _TEST_GROUP_PATTERNS)


def count_ts_entries(spec_dir: Path) -> int:
    """Count TS-NN-N entries in a spec's test_spec.md.

    Returns 0 if the file does not exist.

    Requirements: 46-REQ-4.4
    """
    test_spec = spec_dir / "test_spec.md"
    if not test_spec.exists():
        return 0
    count = 0
    for line in test_spec.read_text().splitlines():
        if line.strip().startswith("### TS-"):
            count += 1
    return count


# ---------------------------------------------------------------------------
# Oracle gating: skip when spec targets only new code
# ---------------------------------------------------------------------------

# Matches file paths in backtick-bold markdown like **`agent_fox/foo.py`** (modified)
_DESIGN_FILE_REF = re.compile(
    r"\*\*`([a-zA-Z0-9_/.\-]+\.\w+)`\*\*\s*\(modified\)",
)


def spec_has_existing_code(spec_path: Path) -> bool:
    """Check whether a spec's design.md references files that already exist.

    Reads design.md, extracts paths marked ``(modified)``, and returns True
    if at least one of those paths exists on disk.  Returns True (safe
    default) when design.md is missing or unreadable so the oracle is not
    accidentally suppressed.
    """
    design_md = spec_path / "design.md"
    try:
        content = design_md.read_text(encoding="utf-8")
    except OSError:
        # No design.md or unreadable — assume code exists (safe default)
        return True

    refs = _DESIGN_FILE_REF.findall(content)
    if not refs:
        # No (modified) references found — nothing for oracle to validate
        return False

    for ref in refs:
        if Path(ref).exists():
            return True

    return False
