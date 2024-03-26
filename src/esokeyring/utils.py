"""Utility functions for the API."""

import uuid

from pydantic import UUID4


def validate_api_key(client_key: UUID4 | str, server_key: UUID4) -> bool:
    """Check that the user key is valid.

    Parameters
    ----------
    user_key:
        The key provided in the request header.
    server_key:
        They key configured on the app configuration.

    Returns
    -------
    A boolean indicating if the keys match.
    """
    if isinstance(client_key, str):
        client_key = uuid.UUID(client_key)
    return client_key == server_key
