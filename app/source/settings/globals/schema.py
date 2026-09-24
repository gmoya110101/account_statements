"""Global settings schema definitions."""

from app.source.settings.base import BaseAppSettings


class GlobalSettings(BaseAppSettings, env_prefix="GLOBAL_"):
    """Global settings."""

    DEBTORS: list[dict[str, str]]
    """List of debtors."""
