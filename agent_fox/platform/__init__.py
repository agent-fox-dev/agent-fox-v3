"""Platform integration layer for agent-fox.

Provides the Platform protocol, GitHubPlatform (REST API),
parse_github_remote utility, and legacy NullPlatform / create_platform
(to be removed in task group 5).
"""

from agent_fox.platform.factory import create_platform
from agent_fox.platform.github import GitHubPlatform, parse_github_remote
from agent_fox.platform.null import NullPlatform
from agent_fox.platform.protocol import Platform

__all__ = [
    "GitHubPlatform",
    "NullPlatform",
    "Platform",
    "create_platform",
    "parse_github_remote",
]
