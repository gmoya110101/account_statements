"""Notifer job settings."""

from app.project_app.repositories.processors.schema import BaseProcessorJobSettings
from app.project_app.repositories.processors.sender.telegram.schema import (
    TelegramSenderJobSettings,
)


class NotifierJobSettings(BaseProcessorJobSettings):
    """Settings for the notifier job."""

    sender: TelegramSenderJobSettings = TelegramSenderJobSettings()
