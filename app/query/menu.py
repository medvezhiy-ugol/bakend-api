from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, List
from app.schemas.menu import (MenuCredits,MenuResponse, 
taxCategoryModel, allergenGroupModel, tagModel, 
itemSizeModel, priceModel,itemModifierGroupModel,ItemsModel,RestrictionsModel,ItemCategorie,ItemModel)


async def write_to_mongo(document: Dict, client: AsyncIOMotorClient):
    menu = client.medvejie_ustie.menu
    #document["_id"] = document.pop("id")
    # добавить for для списка
    result = await menu.update_one({'_id' : document["id"]},{ '$set' :document},True)


async def get_menu_mongo(menu: MenuCredits, client: AsyncIOMotorClient):
    menu = client.medvejie_ustie.menu
    # ХЗ как искать
    resp = await menu.find({'_id': str(menu.externalMenuId)}).to_list(length=None)
    return resp


async def create_new_menu(**resp) -> MenuResponse:
    itemCategories = []
    for itemcategory in resp["itemCategories"]:
        itemDocs = []
        for item in itemcategory["items"]:
            item["taxCategory"] = taxCategoryModel(**item["taxCategory"])
            item["allergenGroups"] = list(map(lambda x: allergenGroupModel(**x),item["allergenGroups"]))
            item["tags"] = list(map(lambda x: tagModel(**x),item["tags"]))
            itemSizes = []
            for itemsize in item["itemSizes"]:
                itemsize["prices"]= list(map(lambda x: priceModel(**x),itemsize["prices"]))
                itemModifierGroups = []
                for itemModifierGroup in itemsize["itemModifierGroups"]:
                    itemModifierGroup["restrictions"] = RestrictionsModel(**itemModifierGroup["restrictions"])
                    items = []
                    for itemin in itemModifierGroup["items"]:
                        itemin["prices"]= list(map(lambda x: priceModel(**x),itemin["prices"]))
                        itemin["restrictions"]= RestrictionsModel(**itemin["restrictions"])
                        itemin["tags"] = list(map(lambda x: tagModel(**x),itemin["tags"]))
                        items.append(ItemsModel(**itemin))
                    itemModifierGroup["items"] = items
                    itemModifierGroups.append(itemModifierGroupModel(**itemModifierGroup))
                itemSizes.append(itemSizeModel(**itemsize))
            itemDoc = await ItemModel(**item).save()
            itemDocs.append(itemDoc)
        itemcategory["item"] = itemDocs
    itemCategories.append(ItemCategorie(**itemcategory))
    return MenuResponse(**resp)