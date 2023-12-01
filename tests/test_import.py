"""Test oid_pocketbase."""

import oid_pocketbase


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(oid_pocketbase.__name__, str)
