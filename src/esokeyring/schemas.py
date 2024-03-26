"""Input and output schemas for the API."""

from pydantic import BaseModel


class LookupResult(BaseModel):
    """Response model for successful lookup."""

    key: str
    secret: str
