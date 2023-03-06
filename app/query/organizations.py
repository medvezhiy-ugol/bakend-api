from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, List
from app.schemas.organizations import Organization

async def get_organization_mongo(client: AsyncIOMotorClient):
    organization = client.medvejie_ustie.organization
    return await organization.find().to_list(length=None)

async def create_organizations(documents: List[Organization], client: AsyncIOMotorClient) -> None:
    orgs = documents["organizations"]
    for org in orgs:
        org["_id"] = org.pop("id")
    organization = client.medvejie_ustie.organization
    result = await organization.insert_many(orgs)
