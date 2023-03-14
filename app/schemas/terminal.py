from pydantic import BaseModel
from typing import List
from uuid import UUID, uuid4
from beanie import Document
from pydantic import Field
    

class TerminalModel(BaseModel):
    organizationIds: List[UUID]
    includeDisabled: bool
    
class ItemsDocument(BaseModel):
    id: UUID
    organizationId: UUID
    name: str
    address: str
    timeZone: str
    
class TerminalGroup(BaseModel):
    organizationId: UUID
    items: List[ItemsDocument]

class TerminalOneModel(BaseModel):
    organizationId: UUID

class TerminalResponse(Document):
    id:UUID = Field(default_factory=uuid4)
    terminalGroups:List[TerminalGroup]
    terminalGroupsInSleep: List[TerminalGroup]