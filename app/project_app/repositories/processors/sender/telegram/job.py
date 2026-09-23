"""Class for Telegram sender job."""

from typing import Any

import requests

from app.project_app.repositories.commons.utils import validate_response
from app.project_app.repositories.processors.sender.base import Base
from app.project_app.repositories.processors.sender.telegram.schema import (
    TelegramSenderJobSettings,
)


class TelegramSenderJob(Base):
    def __init__(self, settings: TelegramSenderJobSettings | dict, **kwargs: Any):
        super().__init__(settings=settings, **kwargs)
        self.settings: TelegramSenderJobSettings

    def _process(self, **kwargs: Any) -> None:
        """Process the Telegram sender job."""
        self.logger(f"{self}: Sending Telegram sender job.")
        url = self.settings.url
        response = requests.post(url=url, **kwargs)
        validate_response(response=response)
        self.logger(f"{self}: Telegram message sent successfully.")

    def execute(
        self,
        **kwargs: Any,
    ) -> Any:
        """Execute the Telegram sender job."""
        self._process(**kwargs)
