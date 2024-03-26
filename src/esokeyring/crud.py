"""Perform keyring operations."""

import keyring


def lookup(service_name: str, username: str) -> str | None:
    """Attempt to look up a password in the keyring."""
    return keyring.get_password(service_name, username)
