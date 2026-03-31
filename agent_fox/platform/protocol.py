"""Platform protocol: abstract issue-tracking operations.

Defines the interface for platform implementations (GitHub, GitLab, etc.).
Scoped to issue tracking only — PR creation has been removed.

Requirements: 61-REQ-8.1, 65-REQ-4.1
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from agent_fox.platform.github import IssueResult


@runtime_checkable
class PlatformProtocol(Protocol):
    """Abstract forge operations for issue and PR management.

    Requirements: 61-REQ-8.1
    """

    async def create_issue(
        self,
        title: str,
        body: str,
        labels: list[str] | None = None,
    ) -> IssueResult: ...

    async def list_issues_by_label(
        self,
        label: str,
        state: str = "open",
    ) -> list[IssueResult]: ...

    async def add_issue_comment(
        self,
        issue_number: int,
        body: str,
    ) -> None: ...

    async def assign_label(
        self,
        issue_number: int,
        label: str,
    ) -> None: ...

    async def close(self) -> None: ...
