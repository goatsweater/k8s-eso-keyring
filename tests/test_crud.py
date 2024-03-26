"""Tests to validate CRUD operations."""

import keyring.backend

from esokeyring import crud


class TestKeyring(keyring.backend.KeyringBackend):
    """A test keyring that outputs a static password."""

    priority = 1

    def set_password(self, service: str, username: str, password: str) -> None:
        pass

    def get_password(self, service: str, username: str) -> str | None:
        return "testvalue"

    def delete_password(self, service: str, username: str) -> None:
        pass


def test_lookup():
    """Ensure that looking up secrets returns the expected value.

    The keyring backend is set to a static backend for testing.
    """
    keyring.set_keyring(TestKeyring())

    result = crud.lookup("someservice", "someuser")
    assert result == "testvalue"
