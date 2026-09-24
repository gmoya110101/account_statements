"""Telegram schema definitions."""

from app.source.settings.base import BaseAppSettings


class TelegramSettings(BaseAppSettings, env_prefix="TELEGRAM_"):
    """Telegram settings."""

    URL: str
    """Base URL for the Telegram API."""

    ENDPOINT: str
    """Endpoint for the Telegram API."""

    TOKEN: str
    """Telegram bot token."""

    MESSAGE: str
    """Message template for Telegram notifications."""