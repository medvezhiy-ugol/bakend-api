from pydantic import BaseModel
from typing import List
from uuid import UUID
    

class TerminalModel(BaseModel):
    organizationIds: List[UUID]
    includeDisabled: bool