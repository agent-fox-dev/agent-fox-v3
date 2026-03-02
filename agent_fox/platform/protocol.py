"""Platform protocol: abstract interface for forge integration.

Defines the Platform Protocol with four async methods for PR lifecycle
operations. Implementations handle the specific forge (GitHub, direct merge).

Requirements: 10-REQ-1.1, 10-REQ-1.2, 10-REQ-1.3, 10-REQ-1.4, 10-REQ-1.5
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Platform(Protocol):
    """Abstract interface for forge integration.

    Implementations handle pull request lifecycle operations. The orchestrator
    calls these methods without knowing whether PRs are being created or
    whether work is being merged directly.
    """

    async def create_pr(
        self,
        branch: str,
        title: str,
        body: str,
        labels: list[str],
    ) -> str:
        """Create a pull request or merge directly.

        Args:
            branch: The feature branch to create a PR from.
            title: PR title.
            body: PR body/description.
            labels: Labels to apply to the PR.

        Returns:
            The PR URL as a string, or empty string if no PR was created.

        Raises:
            IntegrationError: If PR creation fails.
        """
        ...

    async def wait_for_ci(self, pr_url: str, timeout: int) -> bool:
        """Wait for CI checks to pass on a pull request.

        Args:
            pr_url: The PR URL returned by create_pr.
            timeout: Maximum seconds to wait for CI completion.

        Returns:
            True if all CI checks passed, False if any failed or timed out.
        """
        ...

    async def wait_for_review(self, pr_url: str) -> bool:
        """Wait for PR review approval.

        Args:
            pr_url: The PR URL returned by create_pr.

        Returns:
            True if approved, False if changes requested.
        """
        ...

    async def merge_pr(self, pr_url: str) -> None:
        """Merge a pull request.

        Args:
            pr_url: The PR URL returned by create_pr.

        Raises:
            IntegrationError: If merge fails (conflict, branch protection).
        """
        ...
