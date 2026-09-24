"""Main settings for the backend."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class BaseAppSettings(BaseSettings):
    """Base class to use for any settings.

    Subclasses should add only `env_prefix` attribute to organize env variables.
    """

    model_config = SettingsConfigDict(
        use_attribute_docstrings=True,
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
