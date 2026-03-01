"""Configuration system: TOML loading, pydantic models, defaults.

Stub: defines model classes only.
Full implementation in task group 3.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class OrchestratorConfig(BaseModel):
    parallel: int = Field(default=1, ge=1, le=8)
    sync_interval: int = Field(default=5, ge=0)
    hot_load: bool = True
    max_retries: int = Field(default=2, ge=0)
    session_timeout: int = Field(default=30, ge=1)  # minutes
    inter_session_delay: int = Field(default=3, ge=0)  # seconds
    max_cost: float | None = None
    max_sessions: int | None = None


class ModelConfig(BaseModel):
    coding: str = "ADVANCED"
    coordinator: str = "STANDARD"
    memory_extraction: str = "SIMPLE"
    embedding: str = "voyage-3"


class HookConfig(BaseModel):
    pre_code: list[str] = Field(default_factory=list)
    post_code: list[str] = Field(default_factory=list)
    sync_barrier: list[str] = Field(default_factory=list)
    timeout: int = Field(default=300, ge=1)
    modes: dict[str, str] = Field(default_factory=dict)


class SecurityConfig(BaseModel):
    bash_allowlist: list[str] | None = None
    bash_allowlist_extend: list[str] = Field(default_factory=list)


class ThemeConfig(BaseModel):
    playful: bool = True
    header: str = "bold #ff8c00"
    success: str = "bold green"
    error: str = "bold red"
    warning: str = "bold yellow"
    info: str = "#daa520"
    tool: str = "bold #cd853f"
    muted: str = "dim"


class PlatformConfig(BaseModel):
    type: str = "none"
    pr_granularity: str = "session"
    wait_for_ci: bool = False
    wait_for_review: bool = False
    auto_merge: bool = False
    ci_timeout: int = Field(default=600, ge=0)
    labels: list[str] = Field(default_factory=list)


class MemoryConfig(BaseModel):
    model: str = "SIMPLE"


class KnowledgeConfig(BaseModel):
    store_path: str = ".agent-fox/knowledge.duckdb"
    embedding_model: str = "voyage-3"
    embedding_dimensions: int = 1024
    ask_top_k: int = Field(default=20, ge=1)
    ask_synthesis_model: str = "STANDARD"


class AgentFoxConfig(BaseModel):
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)
    models: ModelConfig = Field(default_factory=ModelConfig)
    hooks: HookConfig = Field(default_factory=HookConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    theme: ThemeConfig = Field(default_factory=ThemeConfig)
    platform: PlatformConfig = Field(default_factory=PlatformConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    knowledge: KnowledgeConfig = Field(default_factory=KnowledgeConfig)


def load_config(path: Path | None = None) -> AgentFoxConfig:
    """Load config from TOML, validate, merge with defaults."""
    raise NotImplementedError("load_config not yet implemented")
