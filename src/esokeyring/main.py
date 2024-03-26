"""Provide an API for accessing keyring secrets."""

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import UUID4

from .config import Settings
from .crud import lookup
from .schemas import LookupResult
from .utils import validate_api_key

app = FastAPI()
cfg = Settings()

api_key_header = APIKeyHeader(name="x-api-key")

Instrumentator().instrument(app).expose(app)


@app.get("/health")
async def health_check():
    """Perform a status check to ensure the API is working properly."""
    return {"status": "ok"}


@app.get("/credential/{secret_key}")
async def get_secret(
    secret_key: str, api_key: UUID4 = Depends(api_key_header)
) -> LookupResult:
    """Fetch a secret from the secret store backend."""
    if not validate_api_key(api_key, cfg.key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key."
        )

    secret = lookup(service_name=cfg.service, username=secret_key)
    # If keyring can't find a match it will return None, which is a 404 in HTTP parlance
    if secret is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unknown username f{secret_key}",
        )

    result = LookupResult(key=secret_key, secret=secret)
    return result
