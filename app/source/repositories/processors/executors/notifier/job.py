"""Job for downloading images from dashboard data and sending them via Telegram."""

from typing import Any

from dateutil.relativedelta import relativedelta

from app.source.repositories.base.models import Debtor
from app.source.repositories.commons.utils import DATE_FORMAT, current_datetime
from app.source.repositories.processors.base import BaseProcessorJob
from app.source.repositories.processors.executors.notifier.schema import (
    NotifierJobSettings,
)
from app.source.repositories.processors.sender.telegram.job import (
    TelegramSenderJob,
)
from app.source.repositories.processors.sender.telegram.models import (
    DataModel,
)


class NotifierJob(BaseProcessorJob):
    """Job for sending notifications via Telegram."""

    def __init__(self, settings: NotifierJobSettings | dict):
        """Initialize the notifier job."""

        super().__init__(settings)
        self.settings: NotifierJobSettings
        self.sender: TelegramSenderJob = self._set_sender()

    def _set_next_payment_date(self) -> str:
        """Set the next payment date."""

        today = current_datetime().today()
        base = today.replace(day=1)
        if today.day > 8:
            base += relativedelta(months=1)
        payment_date = (base + relativedelta(days=7)).date()
        return payment_date.strftime(DATE_FORMAT)

    def _set_sender(self) -> TelegramSenderJob:
        """Set the sender job."""
        return TelegramSenderJob(settings=self.settings.sender)

    def _send_message(self, debtor: Debtor) -> None:
        """Send a message via Telegram."""
        message = self.settings.sender.message
        message = message.format(
            DEBTOR_NAME=debtor.name,
            PAYMENT_DATE=self._set_next_payment_date()
        )
        data = DataModel(chat_id=debtor.chat_id, text=message)
        data = data.model_dump(exclude_defaults=True)
        self.sender.execute(data=data)
        self.logger(f"{self}: Message sent for debtor {debtor.name}.")

    def _process(self, debtors: list[Debtor]) -> None:
        """Process the executor job."""
        if not debtors:
            self.logger(f"{self}: No debtors to process.", level="warning")
            return

        self.logger(f"{self}: Processing {len(debtors)} debtors.")
        for debtor in debtors:
            self.logger(f"{self}: Processing debtor {debtor}.")
            self._send_message(debtor=debtor)
        self.logger(f"{self}: Finished processing debtors.")

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
