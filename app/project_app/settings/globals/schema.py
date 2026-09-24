"""Global settings schema definitions."""

from app.project_app.settings.base import BaseAppSettings


class GlobalSettings(BaseAppSettings, env_prefix="GLOBAL_"):
    """Global settings."""

    DEBTORS: list[dict[str, str]]
    """List of debtors."""
