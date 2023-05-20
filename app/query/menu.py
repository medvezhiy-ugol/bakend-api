from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict
from app.schemas.menu import (
    MenuCredits,
    MenuResponse,
    ItemCategorie,
    ItemModel,
)


async def write_to_mongo(document: Dict, client: AsyncIOMotorClient):
    menu = client.medvejie_ustie.menu
    # document["_id"] = document.pop("id")
    # добавить for для списка
    await menu.update_one({"_id": document["id"]}, {"$set": document}, True)



async def create_new_menu(**resp) -> MenuResponse:
    itemCategories = []
    for itemcategory in resp["itemCategories"]:
        itemDocs = []
        category_id = itemcategory["id"]
        for item in itemcategory["items"]:
            item["category_id"] = category_id
            itemDoc = await ItemModel(**dict(item)).save()
            itemDocs.append(itemDoc)
        itemcategory["item"] = itemDocs
    itemCategories.append(ItemCategorie(**itemcategory))
    return resp
