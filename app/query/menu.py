from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict


async def WriteMenu(document: Dict, client: AsyncIOMotorClient):
    document["_id"] = document.pop("id")
    menu = client.medvejie_ustie.menu
    result = await menu.insert_one(document)
    
    

async def get_menu_mongo(client: AsyncIOMotorClient):
    menu = client.medvejie_ustie.menu
    return await menu.find().to_list(length=None)