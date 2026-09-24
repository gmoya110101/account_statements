"""Module defining base interface schema settings."""

from pydantic import BaseModel, ConfigDict

# ----------------------------------------------------------------------------

class BaseSettings(BaseModel):
    """Base interface schema.

    This class serves as a base for defining settings
    for various interface implementations.
    """

    model_config = ConfigDict(extra="allow")
    """Configuration to allow extra fields."""