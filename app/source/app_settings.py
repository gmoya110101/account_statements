"""App settings."""

from pydantic import BaseModel

from app.source.settings import GlobalSettings, GrafanaSettings, TelegramSettings


class AppSettings(BaseModel):
    """All app settings."""

    telegram: TelegramSettings
    """Telegram settings."""

    grafana: GrafanaSettings
    """Grafana settings."""

    global_vars: GlobalSettings
    """Global settings."""


settings = AppSettings(
    telegram=TelegramSettings(),
    grafana=GrafanaSettings(),
    global_vars=GlobalSettings(),
)
