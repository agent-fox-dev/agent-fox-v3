"""Exception hierarchy for agent-fox.

Stub: defines only class names and basic structure.
Full implementation in task group 2.
"""

from __future__ import annotations

from typing import Any


class AgentFoxError(Exception):
    """Base exception for all agent-fox errors."""

    def __init__(self, message: str, **context: Any) -> None:
        super().__init__(message)
        self.context = context


class ConfigError(AgentFoxError): ...


class InitError(AgentFoxError): ...


class PlanError(AgentFoxError): ...


class SessionError(AgentFoxError): ...


class WorkspaceError(AgentFoxError): ...


class IntegrationError(AgentFoxError): ...


class HookError(AgentFoxError): ...


class SessionTimeoutError(AgentFoxError): ...


class CostLimitError(AgentFoxError): ...


class SecurityError(AgentFoxError): ...


class KnowledgeStoreError(AgentFoxError): ...
