"""Infrastructure modules for the project app."""

from app.project_app.settings.grafana.schema import GrafanaSettings
from app.project_app.settings.telegram.schema import TelegramSettings

__all__= [
    "GrafanaSettings",
    "TelegramSettings"
]