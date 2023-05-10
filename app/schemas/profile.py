from typing import Optional
from pydantic import BaseModel, Field


class Profile(BaseModel):
    name: str
    surName: str | None
    middleName: str | None
    phone: str
    birthday: str| None # "like this 2019-08-24 14:15:22.123"
    sex: int  = Field(...,description="Customer sex. 0 - not specified,1 - male, 2 - female.")
