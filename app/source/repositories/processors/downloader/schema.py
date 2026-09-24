"""Downloader job settings."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, HttpUrl, computed_field

from app.source.repositories.processors.schema import BaseProcessorJobSettings


class Type(str, Enum):
    SALE = "Sale"
    LOAN = "Loan"

def to_kebab(name: str) -> str:
    return name.replace("_", "-")
    
class Params(BaseModel):
    """Parameters for the downloader job."""
    model_config = ConfigDict(
            alias_generator=to_kebab,
            populate_by_name=True,
            serialize_by_alias=True,
        )
    
    orgId:int = 1
    _from:str ="now-6h"
    to:str= "now"
    timezone:str= "browser"
    kiosk:str ="1"
    fullPageImage:str ="true"
    width:int= 1200
    height:int= -1
    extra_params: dict = {}
    var_debtor: str = ""
    var_product: str = "$__all"
    var_extra: str = "6000"
    var_type: Type = Type.SALE

class DownloaderJobSettings(BaseProcessorJobSettings):
    """Settings for the downloader job."""
    params: Params = Params()
    url: HttpUrl = HttpUrl("http://localhost:3000")
    timeout: int = 30
    token: str = ""

    @computed_field
    @property
    def headers(self)-> dict:
        return {"Authorization": f"Bearer {self.token}"}
