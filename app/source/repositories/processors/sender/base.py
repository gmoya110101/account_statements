"""Base class for sender implementations."""

from typing import Any

from app.source.repositories.base.base import Base
from app.source.repositories.processors.sender.schema import BaseSenderJobSettings


class BaseSenderJob(Base):
    def __init__(self, settings: BaseSenderJobSettings | dict, **kwargs: Any):
        super().__init__(settings=settings, **kwargs)
        self.settings: BaseSenderJobSettings

    def execute(
        self,
        **_kwargs: Any,
    ) -> Any:
        """Execute the action job."""
        raise NotImplementedError(f"{self}: execute method not implemented.")
