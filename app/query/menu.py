from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, List
from app.schemas.menu import (
    MenuCredits,
    MenuResponse,
    taxCategoryModel,
    allergenGroupModel,
    tagModel,
    itemSizeModel,
    priceModel,
    itemModifierGroupModel,
    ItemsModel,
    RestrictionsModel,
    ItemCategorie,
    ItemModel,
)


async def write_to_mongo(document: Dict, client: AsyncIOMotorClient):
    menu = client.medvejie_ustie.menu
    # document["_id"] = document.pop("id")
    # добавить for для списка
    result = await menu.update_one({"_id": document["id"]}, {"$set": document}, True)


async def get_menu_mongo(menu: MenuCredits, client: AsyncIOMotorClient):
    menu = client.medvejie_ustie.menu
    # ХЗ как искать
    resp = await menu.find({"_id": str(menu.externalMenuId)}).to_list(length=None)
    return resp


async def create_new_menu(**resp) -> MenuResponse:
    itemCategories = []
    for itemcategory in resp["itemCategories"]:
        itemDocs = []
        for item in itemcategory["items"]:
            itemDoc = await ItemModel(**dict(item)).save()
            itemDocs.append(itemDoc)
        itemcategory["item"] = itemDocs
    itemCategories.append(ItemCategorie(**itemcategory))
    return MenuResponse(**resp)
