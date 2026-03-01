"""Task parser tests.

Test Spec: TS-02-3 (parse groups), TS-02-4 (optional marker),
           TS-02-E7 (empty tasks.md), TS-02-E8 (non-contiguous numbers)
Requirements: 02-REQ-2.1, 02-REQ-2.2, 02-REQ-2.3, 02-REQ-2.4,
              02-REQ-2.E1, 02-REQ-2.E2
"""

from __future__ import annotations

from pathlib import Path

from agent_fox.spec.parser import TaskGroupDef, parse_tasks


class TestParseTaskGroups:
    """TS-02-3: Parse task groups from tasks.md."""

    def test_parses_correct_group_count(
        self, tasks_md_standard: Path
    ) -> None:
        """Parser extracts the correct number of task groups."""
        groups = parse_tasks(tasks_md_standard)

        assert len(groups) == 2

    def test_first_group_number(self, tasks_md_standard: Path) -> None:
        """First group has number=1."""
        groups = parse_tasks(tasks_md_standard)

        assert groups[0].number == 1

    def test_first_group_subtask_count(
        self, tasks_md_standard: Path
    ) -> None:
        """First group has 3 subtasks."""
        groups = parse_tasks(tasks_md_standard)

        assert len(groups[0].subtasks) == 3

    def test_first_group_has_title(self, tasks_md_standard: Path) -> None:
        """First group has a non-empty title."""
        groups = parse_tasks(tasks_md_standard)

        assert groups[0].title != ""
        assert "Write failing tests" in groups[0].title

    def test_second_group_number(self, tasks_md_standard: Path) -> None:
        """Second group has number=2."""
        groups = parse_tasks(tasks_md_standard)

        assert groups[1].number == 2

    def test_returns_task_group_def_objects(
        self, tasks_md_standard: Path
    ) -> None:
        """Parser returns TaskGroupDef dataclass instances."""
        groups = parse_tasks(tasks_md_standard)

        assert all(isinstance(g, TaskGroupDef) for g in groups)

    def test_group_has_body(self, tasks_md_standard: Path) -> None:
        """Groups have a non-empty body."""
        groups = parse_tasks(tasks_md_standard)

        # Body should contain the subtask text
        assert groups[0].body != ""

    def test_subtask_ids(self, tasks_md_standard: Path) -> None:
        """Subtask IDs follow N.M pattern."""
        groups = parse_tasks(tasks_md_standard)

        subtask_ids = [s.id for s in groups[0].subtasks]
        assert "1.1" in subtask_ids
        assert "1.2" in subtask_ids
        assert "1.3" in subtask_ids


class TestParseOptionalMarker:
    """TS-02-4: Parse optional task marker."""

    def test_optional_group_detected(
        self, tasks_md_with_optional: Path
    ) -> None:
        """Group marked with * has optional=True."""
        groups = parse_tasks(tasks_md_with_optional)

        optional_group = [g for g in groups if g.number == 3][0]
        assert optional_group.optional is True

    def test_optional_group_title(
        self, tasks_md_with_optional: Path
    ) -> None:
        """Optional group title is parsed correctly (without the *)."""
        groups = parse_tasks(tasks_md_with_optional)

        optional_group = [g for g in groups if g.number == 3][0]
        assert optional_group.title == "Polish and cleanup"

    def test_non_optional_groups(
        self, tasks_md_with_optional: Path
    ) -> None:
        """Groups without * have optional=False."""
        groups = parse_tasks(tasks_md_with_optional)

        non_optional = [g for g in groups if g.number != 3]
        assert all(not g.optional for g in non_optional)

    def test_total_group_count_with_optional(
        self, tasks_md_with_optional: Path
    ) -> None:
        """All groups including optional are parsed."""
        groups = parse_tasks(tasks_md_with_optional)

        assert len(groups) == 4


class TestEmptyTasksMd:
    """TS-02-E7: Empty tasks.md returns empty list."""

    def test_empty_returns_empty_list(self, tasks_md_empty: Path) -> None:
        """tasks.md with no task groups returns empty list."""
        groups = parse_tasks(tasks_md_empty)

        assert len(groups) == 0

    def test_empty_returns_list_type(self, tasks_md_empty: Path) -> None:
        """Return type is a list."""
        groups = parse_tasks(tasks_md_empty)

        assert isinstance(groups, list)


class TestNonContiguousGroupNumbers:
    """TS-02-E8: Parser accepts non-contiguous group numbers."""

    def test_non_contiguous_numbers_accepted(
        self, tasks_md_non_contiguous: Path
    ) -> None:
        """Groups numbered 1, 3, 5 are parsed correctly."""
        groups = parse_tasks(tasks_md_non_contiguous)

        numbers = [g.number for g in groups]
        assert numbers == [1, 3, 5]

    def test_non_contiguous_count(
        self, tasks_md_non_contiguous: Path
    ) -> None:
        """All 3 non-contiguous groups are found."""
        groups = parse_tasks(tasks_md_non_contiguous)

        assert len(groups) == 3
