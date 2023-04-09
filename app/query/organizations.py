from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, List
from app.schemas.organizations import Organization

async def create_organizations(
    documents: List[Organization], client: AsyncIOMotorClient
) -> None:
    list_org =[]
    for org in documents["organizations"]:
        new_org = Organization(**org)
        await new_org.save()
        list_org.append(new_org)
    return list_org
