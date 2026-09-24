"""Base logger class for handling file and console logging."""

import logging as lg
import os
from logging.handlers import RotatingFileHandler
from pprint import pformat
from typing import Any


class WriteLogger:
    """
    Configurable logger class for file and console output.
    """

    def __init__(
        self,
        name: str = "liverpol",
        path: str | None = None,
        filename: str = "main.log",
        str_format: str = "[%(asctime)s][%(levelname)s] %(message)s",
        datefmt: str = "%Y-%m-%dT%H:%M:%SZ",
        level: str | int = "DEBUG",
        rotation_kwargs: dict = {},  # noqa: B006
    ) -> None:
        """
        Initialize the WriteLogger instance with specified configuration.

        """
        self.name = name
        self.filename = None
        if path is not None:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
            if not filename.endswith(".log"):
                filename += ".log"
            self.filename = os.path.join(path, filename)


        self.logger = lg.getLogger(self.name)
        if self.logger.hasHandlers():
            # Avoids duplicated messages from root logger
            self.logger.handlers.clear()

        self.logger.setLevel(self._format_level(level))
        self.formatter = lg.Formatter(str_format, datefmt)

        if self.filename is not None:
            handler = RotatingFileHandler(self.filename, **rotation_kwargs)
        else:
            handler = lg.StreamHandler()
        handler.setFormatter(self.formatter)
        self.handler = handler
        self.logger.addHandler(self.handler)

    def _format_level(self, level: str | int) -> str | int:
        """Format logging level."""
        if isinstance(level, str):
            level = level.upper()
        return level

    def add_module_to_file(self, name: str) -> None | lg.Logger:
        """Create a module logger that shares the same file handler."""
        if self.filename is None:
            return None

        logger = lg.getLogger(name)
        logger.addHandler(self.handler)
        return logger

    def set_level(self, level: str | int) -> None:
        """
        Change the logging level of the logger.

        Updates the minimum logging level for this logger instance.

        Parameters
        ----------
        level : str or int
            New logging level. Can be a string ("DEBUG", "INFO", "WARNING", "ERROR")
            or an integer constant from the logging module.

        Notes
        -----
        Level names are case-insensitive and automatically converted to uppercase.
        """
        self.logger.setLevel(self._format_level(level))

    def exception(self, exception: Exception) -> None:
        """Log an exception with its full traceback information."""
        self.logger.exception(exception)

    def __call__(
        self, *messages: Any, level: str = "info", **pformat_kwargs
    ) -> None:
        """Log one or more messages at the specified logging level."""
        try:
            func = getattr(self.logger, level.lower())
        except Exception as exception:
            self.logger.exception(exception)  # noqa: TRY401
            raise ValueError(
                f"Cannot write log because `level`:{level} doesn't exists"
            ) from exception
        for message in messages:
            if not isinstance(message, str):
                message = pformat(message, **pformat_kwargs)
                message = f"\n{message}"
            func(message)
