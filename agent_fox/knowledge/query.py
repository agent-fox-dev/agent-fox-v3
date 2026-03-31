"""Knowledge query: re-exports from focused query modules.

This module preserves backward compatibility by re-exporting all
public names from query_oracle, query_patterns, and query_temporal.

Requirements: 12-REQ-5.1, 12-REQ-5.2, 12-REQ-5.3, 12-REQ-6.1,
              12-REQ-8.1, 12-REQ-2.E2,
              13-REQ-5.1, 13-REQ-5.2, 13-REQ-5.3, 13-REQ-5.E1,
              13-REQ-4.1, 13-REQ-4.2, 13-REQ-6.1, 13-REQ-6.2, 13-REQ-6.3
"""

from agent_fox.knowledge.query_oracle import Oracle, OracleAnswer
from agent_fox.knowledge.query_patterns import (
    Pattern,
    _assign_confidence,
    detect_patterns,
    render_patterns,
)
from agent_fox.knowledge.query_temporal import (
    Timeline,
    TimelineNode,
    temporal_query,
)

__all__ = [
    "Oracle",
    "OracleAnswer",
    "Pattern",
    "Timeline",
    "TimelineNode",
    "_assign_confidence",
    "detect_patterns",
    "render_patterns",
    "temporal_query",
]
