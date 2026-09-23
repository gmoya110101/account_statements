"""Base class for processor implementations."""

from typing import Any

from app.project_app.repositories.base.base import Base
from app.project_app.repositories.processors.schema import BaseProcessorJobSettings


class BaseProcessorJob(Base):
    def __init__(self, settings: BaseProcessorJobSettings | dict, **kwargs: Any):
        super().__init__(settings=settings, **kwargs)
        self.settings: BaseProcessorJobSettings

    def execute(
        self,
        **_kwargs: Any,
    ) -> Any:
        """Execute the action job."""
        raise NotImplementedError(f"{self}: execute method not implemented.")
