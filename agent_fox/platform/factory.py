"""Platform factory: select the correct Platform implementation.

Provides create_platform(config) which returns either NullPlatform or
GitHubPlatform based on PlatformConfig.type.

Requirements: 10-REQ-5.1, 10-REQ-5.2, 10-REQ-5.3, 10-REQ-5.E1
"""

from __future__ import annotations

from agent_fox.core.config import PlatformConfig  # noqa: F401
from agent_fox.core.errors import ConfigError  # noqa: F401
from agent_fox.platform.protocol import Platform


def create_platform(config: PlatformConfig) -> Platform:
    """Create a Platform implementation based on configuration.

    Args:
        config: Platform configuration from the project config.

    Returns:
        A Platform implementation (NullPlatform or GitHubPlatform).

    Raises:
        ConfigError: If config.type is not a recognized platform type.
    """
    raise NotImplementedError
