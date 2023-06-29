from typing import List
from fastapi import APIRouter, Depends, status, Body, Query, Path
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session
from app.IIko import get_token_iiko, IIko
from app.query.menu import create_new_menu
from app.schemas.menu import MenuCredits, MenuResponse, ItemModel, ItemCategorie, ItemCategorieOut, ItemModelOut
from app.schemas.exception import ProductNotFoundException, MenuNotFoundException
from uuid import UUID
from app.schemas.menu import NewUuid
from beanie import WriteRules


menu_router = APIRouter(tags=["Menu"])


@menu_router.get("/menu")
async def get_menu_id(
    token: str = Depends(get_token_iiko), sesion_iiko: IIko = Depends(IIko)
):
    resp = await sesion_iiko.take_info_menu(token)
    return resp


@menu_router.post(
    "/menu/by_id",
    status_code=status.HTTP_200_OK,
    response_model=List[ItemCategorieOut],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Меню не найдено"}},
)
async def get_menu(
    menu_org: MenuCredits = Body(...),
    session_mongo: AsyncIOMotorClientSession = Depends(get_mongo_session),
):
    # ВОзможно на проде здесь будет ошибка
    menu = await ItemCategorie.find(ItemCategorie.menu_id.id== menu_org.externalMenuId,
                                    fetch_links=True
                                    ).to_list()
    
    if not menu:
        raise MenuNotFoundException(error="Меню не найдено")
    list_category = []
    for itemcategory in menu:
        item_new = ItemCategorieOut(**itemcategory.dict())
        list_category.append(item_new)
    return list_category


@menu_router.get(
    "/menu/category/{category_id}/{skip}/{limit}",
    status_code=status.HTTP_200_OK,
    response_model=List[ItemModel],
    response_model_exclude={"_id"},
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Продуктов в категории не найден"}},
)
async def get_menu(
    category_id: UUID = Path(...),
    skip: int = Path(...),
    limit: int = Path(...),
):
    # ВОзможно на проде здесь будет ошибка
    menu_product = await ItemModel.find(ItemModel.category_id== str(category_id),
                                skip=skip,
                                limit=limit,
                                fetch_links=True
                                ).to_list()
    
    if not menu_product:
        raise MenuNotFoundException(error="Продуктов в категории не найден")
    return menu_product


@menu_router.get(
    "/menu/product/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ItemModel,
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Продукт не найден"}},
)
async def get_product_from_menu(product_id: UUID = Query(...)):
    product = await ItemModel.find(ItemModel.itemId == str(product_id),ItemModel.category_id != None).first_or_none()
    if product is None:
        raise ProductNotFoundException(error="Продукт не найден")
    return product


@menu_router.post(
    "/menu/iiko/by_id/{id_menu}", status_code=status.HTTP_200_OK
    
)
async def take_menu(
    token: str = Depends(get_token_iiko),
    session_mdb: AsyncIOMotorClientSession = Depends(get_mongo_session),
    id_menu: int = Path(...),
    sesion_iiko: IIko = Depends(IIko),
):
    new_menu = await sesion_iiko.take_menu_byid(token, id_menu)
    menu_resp: MenuResponse = MenuResponse( ** await create_new_menu(**new_menu))
    await menu_resp.save(link_rule= WriteRules.WRITE)
    return new_menu
