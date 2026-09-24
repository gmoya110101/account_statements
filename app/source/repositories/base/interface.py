"""Interface for repository implementations."""

from abc import ABC, abstractmethod
from types import ModuleType
from typing import Any

from pydantic import BaseModel


class Interface(ABC):

    @abstractmethod
    def _set_settings(self,settings: BaseModel | dict ) -> BaseModel:
        ...

    @abstractmethod
    def _get_schema_module(self) -> ModuleType:
        ...

    @abstractmethod
    def _get_schema_class(self) -> type[BaseModel]:
        ...

    @abstractmethod
    def _process(self, *_args: Any, **_kwargs: Any) -> Any:
        ...

    @abstractmethod
    def execute(self, *_args: Any, **_kwargs: Any) -> Any:
        ...