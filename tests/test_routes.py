"""API route related tests."""

import os
import uuid

import keyring.backend
from fastapi.testclient import TestClient

from esokeyring import main, schemas

client = TestClient(main.app)

class TestKeyring(keyring.backend.KeyringBackend):
    """A test keyring that outputs a static password except for a specifc condition."""

    priority = 1

    def set_password(self, service: str, username: str, password: str) -> None:
        pass

    def get_password(self, service: str, username: str) -> str | None:
        if username != "missing":
            return "knownvalue"
        else:
            return None

    def delete_password(self, service: str, username: str) -> None:
        pass


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_fetch_existing_credential():
    keyring.set_keyring(TestKeyring())
    result = schemas.LookupResult(key="knownkey", secret="knownvalue")

    headers = {"x-api-key": os.getenv("KAPI_KEY")}
    response = client.get("/credential/knownkey", headers=headers)

    assert response.status_code == 200
    assert response.json() == result.model_dump()


def test_fetch_missing_credential():
    keyring.set_keyring(TestKeyring())

    headers = {"x-api-key": os.getenv("KAPI_KEY")}
    response = client.get("/credential/missing", headers=headers)

    assert response.status_code == 404


def test_fetch_credential_bad_key():
    keyring.set_keyring(TestKeyring())

    headers = {"x-api-key": str(uuid.uuid4())}
    response = client.get("/credential/missing", headers=headers)

    assert response.status_code == 401


def test_fetch_credential_without_api_key():
    result = client.get("/credential/doesntmatter")

    assert result.status_code == 403
