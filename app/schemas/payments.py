from uuid import UUID
from pydantic import BaseModel


class Organiztion(BaseModel):
    org: UUID