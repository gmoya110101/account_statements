"""App settings."""

from pydantic import BaseModel

from app.project_app.settings import GrafanaSettings, TelegramSettings


class AppSettings(BaseModel):
    """All app settings."""

    telegram: TelegramSettings
    """Telegram settings."""

    grafana: GrafanaSettings
    """Grafana settings."""


settings = AppSettings(
    telegram=TelegramSettings(),
    grafana=GrafanaSettings(),
)
