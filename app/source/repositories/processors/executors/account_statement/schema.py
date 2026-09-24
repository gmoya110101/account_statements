"""Downloader job settings."""

from pathlib import Path

from pydantic import BaseModel, model_validator

from app.source.repositories.processors.downloader.schema import (
    DownloaderJobSettings,
)
from app.source.repositories.processors.schema import BaseProcessorJobSettings
from app.source.repositories.processors.sender.telegram.schema import (
    TelegramSenderJobSettings,
)


class SaveLocalSettings(BaseModel):
    """Settings for saving images locally."""

    path: Path = Path("./images/")

    @model_validator(mode="after")
    def is_a_dir(self) -> "SaveLocalSettings":
        if self.path.exists() and not self.path.is_dir():
            raise ValueError(f"Path exists but is not a directory: {self.path}")
        self.path.mkdir(parents=True, exist_ok=True)
        return self


class AccountStatementJobSettings(BaseProcessorJobSettings):
    """Settings for the executor job."""

    downloader: DownloaderJobSettings = DownloaderJobSettings()
    sender: TelegramSenderJobSettings = TelegramSenderJobSettings()
    save_local: SaveLocalSettings | None = None
