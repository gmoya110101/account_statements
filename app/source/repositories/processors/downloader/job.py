"""Job for downloading images from dashboard data."""

from typing import Any

import requests

from app.source.repositories.commons.utils import validate_response
from app.source.repositories.processors.base import BaseProcessorJob
from app.source.repositories.processors.downloader.schema import (
    DownloaderJobSettings,
)


class DownloaderJob(BaseProcessorJob):
    def __init__(self, settings: DownloaderJobSettings | dict):
        super().__init__(settings)
        self.settings: DownloaderJobSettings

    def _get_dashboard_image(self, debtor: str) -> bytes:
        """Download the dashboard image for the specified client."""
        

        params = self.settings.params
        params.var_debtor=debtor
        self.logger(f"{self}: Downloading dashboard image for debtor: {debtor}")
        response = requests.get(
            url=self.settings.url,
            params=params.model_dump(),
            headers=self.settings.headers,
            timeout=self.settings.timeout,
        )
        validate_response(response)
        self.logger(f"{self}: Finished downloading dashboard image for debtor: {debtor}")
        return response.content

    def execute(self, debtor: str, **kwargs: Any) -> bytes:
        """Execute the downloader job."""
        return self._get_dashboard_image(debtor=debtor)
