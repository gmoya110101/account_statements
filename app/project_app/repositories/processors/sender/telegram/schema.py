"""Schema for Telegram sender implementations."""

from pydantic import computed_field, field_validator

from app.project_app.repositories.processors.sender.schema import BaseSenderJobSettings


class TelegramSenderJobSettings(BaseSenderJobSettings):
    """Schema for Telegram sender job settings."""

    base_url:str ="https://api.telegram.org/bot{TOKEN}"
    """URL for sending photos via Telegram API"""
    endpoint:str = "/sendPhoto"
    """Endpoint for the Telegram API"""
    token:str = ""
    """Telegram bot token"""
    message:str="Hello, this is a test message!"
    """Default message for Telegram notifications"""

    @computed_field
    @property
    def url(self)->str:
        """Compute the URL for sending photos via Telegram API."""
        base_url = self.base_url.format(TOKEN=self.token)
        return f"{base_url}{self.endpoint}"

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Validate the base URL."""
        if "{TOKEN}" not in v:
            raise ValueError("Invalid base URL. Please include {TOKEN} placeholder.")
        return v

