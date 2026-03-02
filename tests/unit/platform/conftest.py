"""Fixtures for platform integration tests.

Provides mock subprocess, NullPlatform and GitHubPlatform instances,
and default PlatformConfig for testing.
"""

from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from agent_fox.core.config import PlatformConfig
from agent_fox.platform.null import NullPlatform


def _make_completed_process(
    *,
    returncode: int = 0,
    stdout: str = "",
    stderr: str = "",
) -> subprocess.CompletedProcess[str]:
    """Create a subprocess.CompletedProcess with the given values."""
    return subprocess.CompletedProcess(
        args=[],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


@pytest.fixture
def mock_subprocess():
    """Patch subprocess.run and return the mock.

    The mock is set up to return a successful CompletedProcess by default.
    Callers can configure return values for specific commands.
    """
    with patch("agent_fox.platform.null.subprocess.run") as mock_run:
        mock_run.return_value = _make_completed_process()
        yield mock_run


@pytest.fixture
def mock_gh_subprocess():
    """Patch subprocess.run for GitHubPlatform and return the mock.

    The mock is set up to return a successful CompletedProcess by default.
    Also patches shutil.which and gh auth status for init.
    """
    with (
        patch("agent_fox.platform.github.subprocess.run") as mock_run,
        patch("agent_fox.platform.github.shutil.which", return_value="/usr/bin/gh"),
    ):
        mock_run.return_value = _make_completed_process()
        yield mock_run


@pytest.fixture
def null_platform() -> NullPlatform:
    """A NullPlatform instance with default develop branch."""
    return NullPlatform()


@pytest.fixture
def github_platform(mock_gh_subprocess: MagicMock):
    """A GitHubPlatform instance with mocked gh availability.

    The mock_gh_subprocess fixture patches shutil.which and subprocess.run
    so GitHubPlatform.__init__ succeeds without real gh CLI.
    """
    from agent_fox.platform.github import GitHubPlatform

    return GitHubPlatform()


@pytest.fixture
def platform_config() -> PlatformConfig:
    """Default PlatformConfig for testing."""
    return PlatformConfig()
