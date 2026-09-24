"""Common models for the application."""

from pydantic import BaseModel


class Debtor(BaseModel):
    """A debtor with a name and ID."""
    
    name: str
    chat_id: str