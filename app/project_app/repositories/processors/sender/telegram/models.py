"""Models for Telegram sender implementations."""

from enum import Enum

from pydantic import BaseModel


class Modes(str, Enum):
    MARKDOWN = "Markdown"
    HTML = "HTML"


class FilesModel(BaseModel):
    """Model for files to be sent via Telegram."""

    photo: bytes
    """The photo to be sent."""


class DataModel(BaseModel):
    """Model for data to be sent via Telegram."""

    chat_id: str
    """The ID of the chat to send the message to."""
    text: str | None = None
    """The text of the message."""
    caption: str | None = None
    """The caption for the photo."""
    parse_mode: Modes = Modes.HTML
    """The parse mode for the message."""
