from pydantic import BaseModel
from uuid import UUID

class MenuCredits(BaseModel):
    organizationIds: UUID
    externalMenuId: str