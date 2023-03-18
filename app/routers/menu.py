from fastapi import APIRouter, Depends, status, Body, Query
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session
from app.IIko import get_token_iiko, IIko
from app.query.menu import get_menu_mongo, create_new_menu
from app.schemas.menu import MenuCredits, MenuResponse, ItemModel
from app.schemas.exception import ProductNotFoundException
from uuid import UUID


menu_router = APIRouter(tags=["Menu"])



@menu_router.get("/menu")
async def get_menu_id(token: str = Depends(get_token_iiko),
                      sesion_iiko: IIko = Depends(IIko)):
    resp = await sesion_iiko.take_info_menu(token)
    return resp


@menu_router.post("/menu/by_id",
    status_code=status.HTTP_200_OK,
    response_model=MenuResponse)
async def get_menu(menu_org : MenuCredits = Body(...),
                   session_mongo: AsyncIOMotorClientSession = Depends(get_mongo_session)):
    # ВОзможно на проде здесь будет ошибка
    menu = await MenuResponse.get(menu_org.externalMenuId)
    return menu

@menu_router.get("/menu/product/{id}",
                 status_code=status.HTTP_200_OK,
                 response_model=ItemModel)
async def get_product_from_menu(product_id: UUID = Query(...)):
    product = await ItemModel.find(ItemModel.itemId==product_id).first_or_none()
    if product is None:
        raise ProductNotFoundException(error="Продукт не найден")
    return product


@menu_router.post("/menu/iiko/by_id",
                  status_code=status.HTTP_200_OK,
                  response_model=MenuResponse)
async def take_menu(token: str = Depends(get_token_iiko),
                    session_mdb:AsyncIOMotorClientSession = Depends(get_mongo_session),
                    sesion_iiko: IIko = Depends(IIko)):
    new_menu = await sesion_iiko.take_menu_byid(token)
    menu_resp : MenuResponse = await create_new_menu(**new_menu)
    await menu_resp.save()
    return menu_resp
