"""Utility functions for common operations."""

import datetime as dt
import json
import os
from pathlib import Path

import requests

from app.project_app.repositories.base.base_logger import WriteLogger

logger = WriteLogger(name=__name__)

DATE_FORMAT = "%Y-%m-%d"

def read_json_file(path:str):
    """Read a JSON file and return its contents."""
    logger.debug(f"Reading JSON file: {path}")
    with open(path) as f:
        return json.load(f)

def current_datetime() -> dt.datetime:
    """Return the current datetime in UTC timezone."""
    return dt.datetime.now(tz=dt.UTC)

def validate_response(response: requests.Response)->None:
    """Validate the response."""
    if response.status_code != requests.status_codes.codes.ok:
        raise ValueError(f"Invalid response: {response.status_code} -> {response.text}")

def create_local_dir(path: Path)->None:
    if not path.exists():
        logger("Creating local directory.")
        os.makedirs(path)
        return
    logger(f"Local directory {path} already exists.")

def save_file_in_local(path:str, content: bytes):
    with open(path, "wb") as f:
        f.write(content)
        logger(f"File saved in {path}.")