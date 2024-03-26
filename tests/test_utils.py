"""Test utility functions."""

import uuid

from esokeyring import utils


def test_api_key_validation():
    """Ensure API keys are properly validated."""
    fakekey = uuid.uuid4()
    otherkey = uuid.uuid4()

    # Matching keys should successfully validate
    result = utils.validate_api_key(fakekey, fakekey)
    assert result is True

    # Validate even when the client key is a string
    result = utils.validate_api_key(str(fakekey), fakekey)
    assert result is True

    # Non-matching keys should fail validation
    result = utils.validate_api_key(fakekey, otherkey)
    assert result is False
