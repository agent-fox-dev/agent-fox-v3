"""Tests for Platform protocol definition and structural conformance.

Test Spec: TS-10-1 (protocol methods), TS-10-2 (NullPlatform satisfies protocol)
Requirements: 10-REQ-1.1, 10-REQ-1.2, 10-REQ-1.3, 10-REQ-1.4, 10-REQ-1.5,
              10-REQ-2.1
"""

from __future__ import annotations

import inspect

from agent_fox.platform.null import NullPlatform
from agent_fox.platform.protocol import Platform


class TestPlatformProtocolMethods:
    """TS-10-1: Platform protocol defines required methods.

    Requirement: 10-REQ-1.1
    Verify the Platform protocol declares all four required async methods
    with correct signatures.
    """

    def test_has_create_pr_method(self) -> None:
        """Platform protocol has a create_pr method."""
        assert hasattr(Platform, "create_pr")

    def test_has_wait_for_ci_method(self) -> None:
        """Platform protocol has a wait_for_ci method."""
        assert hasattr(Platform, "wait_for_ci")

    def test_has_wait_for_review_method(self) -> None:
        """Platform protocol has a wait_for_review method."""
        assert hasattr(Platform, "wait_for_review")

    def test_has_merge_pr_method(self) -> None:
        """Platform protocol has a merge_pr method."""
        assert hasattr(Platform, "merge_pr")

    def test_create_pr_is_coroutine(self) -> None:
        """create_pr is an async method (10-REQ-1.2)."""
        assert inspect.iscoroutinefunction(Platform.create_pr)

    def test_wait_for_ci_is_coroutine(self) -> None:
        """wait_for_ci is an async method (10-REQ-1.3)."""
        assert inspect.iscoroutinefunction(Platform.wait_for_ci)

    def test_wait_for_review_is_coroutine(self) -> None:
        """wait_for_review is an async method (10-REQ-1.4)."""
        assert inspect.iscoroutinefunction(Platform.wait_for_review)

    def test_merge_pr_is_coroutine(self) -> None:
        """merge_pr is an async method (10-REQ-1.5)."""
        assert inspect.iscoroutinefunction(Platform.merge_pr)

    def test_create_pr_signature(self) -> None:
        """create_pr accepts branch, title, body, labels (10-REQ-1.2)."""
        sig = inspect.signature(Platform.create_pr)
        params = list(sig.parameters.keys())
        assert "branch" in params
        assert "title" in params
        assert "body" in params
        assert "labels" in params

    def test_wait_for_ci_signature(self) -> None:
        """wait_for_ci accepts pr_url and timeout (10-REQ-1.3)."""
        sig = inspect.signature(Platform.wait_for_ci)
        params = list(sig.parameters.keys())
        assert "pr_url" in params
        assert "timeout" in params

    def test_wait_for_review_signature(self) -> None:
        """wait_for_review accepts pr_url (10-REQ-1.4)."""
        sig = inspect.signature(Platform.wait_for_review)
        params = list(sig.parameters.keys())
        assert "pr_url" in params

    def test_merge_pr_signature(self) -> None:
        """merge_pr accepts pr_url (10-REQ-1.5)."""
        sig = inspect.signature(Platform.merge_pr)
        params = list(sig.parameters.keys())
        assert "pr_url" in params


class TestNullPlatformSatisfiesProtocol:
    """TS-10-2: NullPlatform satisfies Platform protocol.

    Requirement: 10-REQ-2.1
    Verify NullPlatform is a structural subtype of Platform via
    runtime_checkable isinstance check.
    """

    def test_null_platform_is_instance_of_platform(self) -> None:
        """NullPlatform() passes isinstance check against Platform."""
        null = NullPlatform()
        assert isinstance(null, Platform)
