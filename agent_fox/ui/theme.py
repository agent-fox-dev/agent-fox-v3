"""Terminal theme system with Rich styles.

Stub: defines interfaces only.
Full implementation in task group 4.
"""

from __future__ import annotations

from dataclasses import dataclass

from agent_fox.core.config import ThemeConfig


@dataclass
class AppTheme:
    """Themed console output with configurable color roles."""

    config: ThemeConfig

    def styled(self, text: str, role: str) -> str:
        """Return text styled for the given role."""
        raise NotImplementedError("styled not yet implemented")

    def print(self, text: str, role: str = "info") -> None:
        """Print styled text to console."""
        raise NotImplementedError("print not yet implemented")

    def success(self, text: str) -> None:
        """Print a success message."""
        raise NotImplementedError("success not yet implemented")

    def error(self, text: str) -> None:
        """Print an error message."""
        raise NotImplementedError("error not yet implemented")

    def warning(self, text: str) -> None:
        """Print a warning message."""
        raise NotImplementedError("warning not yet implemented")

    def header(self, text: str) -> None:
        """Print a header message."""
        raise NotImplementedError("header not yet implemented")

    def playful(self, key: str) -> str:
        """Return playful or neutral message based on config."""
        raise NotImplementedError("playful not yet implemented")


def create_theme(config: ThemeConfig) -> AppTheme:
    """Create an AppTheme from configuration."""
    raise NotImplementedError("create_theme not yet implemented")
