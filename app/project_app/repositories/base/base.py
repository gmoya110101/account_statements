"""Base interface for a single unit of work."""

import re
from importlib import import_module
from types import ModuleType
from typing import Any

from pydantic import BaseModel

from app.project_app.repositories.base.base_logger import WriteLogger
from app.project_app.repositories.base.interface import Interface
from app.project_app.repositories.base.schema import BaseSettings


class Base(Interface):
    """Base interface for a single unit of work."""

    def __init__(
        self,
        settings: BaseSettings | BaseModel | dict,
        *_args: Any,
        **_kwargs: Any,
    ) -> None:
        """Initialize the Base with settings."""
        self.logger = WriteLogger(name=self.__class__.__name__)
        self.settings = self._set_settings(settings)

    def __repr__(self) -> str:
        """Return a string representation of the Base."""
        return f"{self.__class__.__name__}"

    def _get_schema_module(self) -> ModuleType:
        """Get the schema module for the interface."""
        self.logger(f"{self}: Getting interface schema module", level="debug")
        module_name = re.sub(r"\.job$|\.base$", ".schema", self.__module__)
        try:
            module = import_module(module_name)
        except Exception as exc:
            self.logger(
                f"{self}: Interface doesn`t have a schema module={module_name}, returning default response",
                level="error",
            )
            raise exc  # noqa: TRY201
        self.logger(
            f"{self}: Interface schema module={module_name} successfully loaded",
            level="debug",
        )
        return module

    def _get_schema_class(self) -> type[BaseSettings]:
        """Get the schema class for the interface."""
        self.logger(f"{self}: Getting interface schema class", level="debug")
        class_name = f"{self.__class__.__name__}Settings"
        module = self._get_schema_module()

        _class = getattr(module, class_name, None)
        if _class is None:
            raise AttributeError(f"Module {module.__name__} does not have a {class_name} model")
        if not issubclass(_class, BaseSettings):
            raise TypeError(f"{_class} is not a subclass of BaseSettings")
        self.logger(f"{self}: Schema class {class_name} successfully loaded", level="debug")
        return _class

    def _set_settings(
        self, settings: BaseSettings | BaseModel | dict
    ) -> BaseSettings | BaseModel:
        """Set and validate the interface settings."""
        schema_class = self._get_schema_class()
        if isinstance(settings, dict):
            self.logger(f"{self}: Validating settings from dict", level="debug")
            return schema_class.model_validate(settings)
        return schema_class.model_validate(settings.model_dump())

    def _process(self, *_args: Any, **_kwargs: Any) -> None:
        """Process the unit of work.

        This method should be implemented by subclasses to define
        the specific work to be performed.
        """
        raise NotImplementedError(f"{self}: This method should be implemented by subclasses.")

    def execute(self, *_args: Any, **_kwargs: Any) -> Any:
        """Execute the unit of work.

        This method should be implemented by subclasses to define
        the specific work to be performed.
        """
        raise NotImplementedError(f"{self}: This method should be implemented by subclasses.")

