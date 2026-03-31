"""Tests for field-level validation in fact extraction parsing.

Regression tests for GitHub issue #186: extraction responses must
enforce string length limits and keyword constraints.
"""

from __future__ import annotations

import json

import pytest

from agent_fox.core.llm_validation import (
    MAX_CONTENT_LENGTH,
    MAX_KEYWORD_LENGTH,
    MAX_KEYWORDS,
    ResponseTooLargeError,
)
from agent_fox.knowledge.extraction import _parse_extraction_response


class TestExtractionFieldValidation:
    """_parse_extraction_response enforces field-level constraints."""

    def test_normal_response_parses_correctly(self) -> None:
        raw = json.dumps(
            [
                {
                    "content": "Test fact",
                    "category": "gotcha",
                    "confidence": "high",
                    "keywords": ["python", "testing"],
                }
            ]
        )
        facts = _parse_extraction_response(raw, "spec-1", "session-1")
        assert len(facts) == 1
        assert facts[0].content == "Test fact"

    def test_oversized_content_truncated(self) -> None:
        raw = json.dumps(
            [
                {
                    "content": "x" * (MAX_CONTENT_LENGTH + 1000),
                    "category": "gotcha",
                    "confidence": "high",
                    "keywords": ["test"],
                }
            ]
        )
        facts = _parse_extraction_response(raw, "spec-1", "session-1")
        assert len(facts) == 1
        assert len(facts[0].content) == MAX_CONTENT_LENGTH

    def test_excessive_keywords_capped(self) -> None:
        raw = json.dumps(
            [
                {
                    "content": "Test fact",
                    "category": "gotcha",
                    "confidence": "high",
                    "keywords": [f"kw{i}" for i in range(50)],
                }
            ]
        )
        facts = _parse_extraction_response(raw, "spec-1", "session-1")
        assert len(facts) == 1
        assert len(facts[0].keywords) == MAX_KEYWORDS

    def test_long_keyword_truncated(self) -> None:
        raw = json.dumps(
            [
                {
                    "content": "Test fact",
                    "category": "gotcha",
                    "confidence": "high",
                    "keywords": ["a" * (MAX_KEYWORD_LENGTH + 100)],
                }
            ]
        )
        facts = _parse_extraction_response(raw, "spec-1", "session-1")
        assert len(facts[0].keywords[0]) == MAX_KEYWORD_LENGTH

    def test_non_string_keywords_dropped(self) -> None:
        raw = json.dumps(
            [
                {
                    "content": "Test fact",
                    "category": "gotcha",
                    "confidence": "high",
                    "keywords": ["valid", 123, None],
                }
            ]
        )
        facts = _parse_extraction_response(raw, "spec-1", "session-1")
        assert facts[0].keywords == ["valid"]

    def test_oversized_raw_response_rejected(self) -> None:
        """A raw response exceeding the size limit raises before parsing."""
        huge = json.dumps([{"content": "x" * 600_000}])
        with pytest.raises(ResponseTooLargeError):
            _parse_extraction_response(huge, "spec-1", "session-1")
