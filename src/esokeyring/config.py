"""Configuration for the API."""

from pydantic import UUID4
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration of the API."""

    service: str = "esokeyring"

    key: UUID4

    model_config = SettingsConfigDict(env_prefix="KAPI_", env_file=".env")
