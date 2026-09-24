"""Grafana schema definitions."""

from app.source.settings.base import BaseAppSettings


class GrafanaSettings(BaseAppSettings, env_prefix="GRAFANA_"):
    """Grafana settings."""
    URL: str
    """Base URL for the Grafana API."""
    TOKEN: str
    """Grafana API token."""
