"""Tests for LLM response validation utilities.

Regression tests for GitHub issue #186: LLM JSON responses
deserialized without schema validation.
"""

from __future__ import annotations

import pytest

from agent_fox.core.llm_validation import (
    MAX_CONTENT_LENGTH,
    MAX_KEYWORD_LENGTH,
    MAX_KEYWORDS,
    ResponseTooLargeError,
    check_response_size,
    truncate_field,
    validate_keywords,
)


class TestCheckResponseSize:
    """Raw response size gating."""

    def test_accepts_small_response(self) -> None:
        check_response_size("short", max_bytes=1000)  # no exception

    def test_rejects_oversized_response(self) -> None:
        with pytest.raises(ResponseTooLargeError, match="exceeding"):
            check_response_size("x" * 1000, max_bytes=100)

    def test_exact_limit_accepted(self) -> None:
        text = "a" * 100
        check_response_size(text, max_bytes=100)  # no exception

    def test_one_over_limit_rejected(self) -> None:
        text = "a" * 101
        with pytest.raises(ResponseTooLargeError):
            check_response_size(text, max_bytes=100)

    def test_counts_utf8_bytes_not_chars(self) -> None:
        """Multi-byte characters count as multiple bytes."""
        # Each emoji is 4 bytes in UTF-8
        emoji_text = "\U0001f600" * 10  # 10 chars, 40 bytes
        check_response_size(emoji_text, max_bytes=40)
        with pytest.raises(ResponseTooLargeError):
            check_response_size(emoji_text, max_bytes=39)

    def test_error_message_includes_context(self) -> None:
        with pytest.raises(ResponseTooLargeError, match="test context"):
            check_response_size("x" * 200, max_bytes=100, context="test context")


class TestTruncateField:
    """String field truncation."""

    def test_short_string_unchanged(self) -> None:
        assert truncate_field("hello", max_length=100, field_name="f") == "hello"

    def test_long_string_truncated(self) -> None:
        result = truncate_field("x" * 200, max_length=50, field_name="content")
        assert len(result) == 50
        assert result == "x" * 50

    def test_exact_length_unchanged(self) -> None:
        text = "a" * 100
        assert truncate_field(text, max_length=100, field_name="f") == text

    def test_empty_string_unchanged(self) -> None:
        assert truncate_field("", max_length=100, field_name="f") == ""


class TestValidateKeywords:
    """Keyword list validation."""

    def test_valid_keywords_pass_through(self) -> None:
        kws = ["python", "testing"]
        assert validate_keywords(kws) == ["python", "testing"]

    def test_non_string_items_dropped(self) -> None:
        kws = ["valid", 123, None, "also_valid", True]
        result = validate_keywords(kws)
        assert result == ["valid", "also_valid"]

    def test_keywords_capped_at_max_count(self) -> None:
        kws = [f"kw{i}" for i in range(50)]
        result = validate_keywords(kws, max_count=5)
        assert len(result) == 5

    def test_long_keywords_truncated(self) -> None:
        kws = ["x" * 200]
        result = validate_keywords(kws, max_length=10)
        assert result == ["x" * 10]

    def test_empty_list(self) -> None:
        assert validate_keywords([]) == []

    def test_default_limits(self) -> None:
        """Default limits match module constants."""
        kws = [f"kw{i}" for i in range(MAX_KEYWORDS + 5)]
        result = validate_keywords(kws)
        assert len(result) == MAX_KEYWORDS

    def test_keyword_at_max_length_unchanged(self) -> None:
        kw = "a" * MAX_KEYWORD_LENGTH
        assert validate_keywords([kw])[0] == kw


class TestMaxContentLengthConstant:
    """Verify MAX_CONTENT_LENGTH is reasonable."""

    def test_max_content_length_is_5000(self) -> None:
        assert MAX_CONTENT_LENGTH == 5000
