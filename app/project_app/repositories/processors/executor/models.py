"""Models for the executor job."""


from pydantic import BaseModel


class Debtor(BaseModel):
    """A debtor with a name and ID."""
    
    name: str
    chat_id: str