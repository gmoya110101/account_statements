"""Job for downloading images from dashboard data."""

from typing import Any

from app.project_app.repositories.commons.utils import (
    create_local_dir,
    current_datetime,
    save_file_in_local,
)
from app.project_app.repositories.processors.base import BaseProcessorJob
from app.project_app.repositories.processors.downloader.job import DownloaderJob
from app.project_app.repositories.processors.executor.models import Debtor
from app.project_app.repositories.processors.executor.schema import (
    ExecutorJobSettings,
)
from app.project_app.repositories.processors.sender.telegram.job import (
    TelegramSenderJob,
)
from app.project_app.repositories.processors.sender.telegram.models import (
    DataModel,
    FilesModel,
)

_DATE_FORMAT = "%Y-%m-%d"
current_date = current_datetime()
date_str = current_date.strftime(format=_DATE_FORMAT)


class ExecutorJob(BaseProcessorJob):
    def __init__(self, settings: ExecutorJobSettings | dict):
        super().__init__(settings)
        self.settings: ExecutorJobSettings
        self.downloader: DownloaderJob = self._set_downloader()
        self.sender: TelegramSenderJob = self._set_sender()

    def _set_downloader(self) -> DownloaderJob:
        """Set the downloader job."""
        return DownloaderJob(settings=self.settings.downloader)

    def _set_sender(self) -> TelegramSenderJob:
        """Set the sender job."""
        return TelegramSenderJob(settings=self.settings.sender)

    def _save_image_in_local(self, image: bytes, debtor_name: str) -> None:
        """Save the downloaded image in local storage."""

        base_path = self.settings.save_local.path
        path = base_path / date_str

        create_local_dir(path)
        self.logger(f"{self}: Saving image for debtor {debtor_name} in {path}.")
        full_path: str = path / f"{debtor_name}.jpg"
        save_file_in_local(full_path, image)

    def _send_message(self, debtor: Debtor, image: bytes) -> None:
        """Send a message via Telegram."""
        message = self.settings.sender.message
        message = message.format(DEBTOR_NAME=debtor.name)
        files = FilesModel(photo=image)
        files = files.model_dump()
        data = DataModel(chat_id=debtor.chat_id, caption=message)
        data = data.model_dump(exclude_defaults=True)
        self.sender.execute(files=files, data=data)
        self.logger(f"{self}: Message sent for debtor {debtor.name}.")

    def _process(self, debtors: list[Debtor]) -> None:
        """Process the executor job."""
        if not debtors:
            self.logger(f"{self}: No debtors to process.", level="warning")
            return

        self.logger(f"{self}: Processing {len(debtors)} debtors.")
        for debtor in debtors:
            self.logger(f"{self}: Processing debtor {debtor}.")
            image = self.downloader.execute(
                debtor=debtor.name,
            )
            if self.settings.save_local:
                self._save_image_in_local(image=image, debtor=debtor)
            self._send_message(debtor=debtor, image=image)

    def execute(
        self,
        debtors: list[Debtor | dict[str, str]],
        **_kwargs: Any,
    ) -> None:
        """Execute the executor job."""

        if not debtors:
            self.logger(f"{self}: No debtors to process.", level="warning")
            return

        if isinstance(debtors[0], dict):
            self.logger(f"{self}: Converting debtors to Debtor objects.")
            debtors = [Debtor(**debtor) for debtor in debtors]

        self.logger(f"{self}: Executor job started.")
        self._process(debtors=debtors)
        self.logger(f"{self}: Executor job completed.")
