"""Notifer job settings."""

from app.source.repositories.processors.schema import BaseProcessorJobSettings
from app.source.repositories.processors.sender.telegram.schema import (
    TelegramSenderJobSettings,
)


class NotifierJobSettings(BaseProcessorJobSettings):
    """Settings for the notifier job."""

    sender: TelegramSenderJobSettings = TelegramSenderJobSettings()
