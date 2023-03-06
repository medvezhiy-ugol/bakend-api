from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session
from app.IIko import get_token_iiko, IIko
from app.query.menu import WriteMenu,get_menu_mongo
from app.db.connection import get_mongo_session



menu_router = APIRouter(tags=["Menu"])


@menu_router.get("/menu",
    status_code=status.HTTP_200_OK)
async def get_menu(session_mongo: AsyncIOMotorClientSession = Depends(get_mongo_session)):
    menu = await get_menu_mongo(session_mongo)
    menu[0].pop("_id") # УДаляю ObjectID так как он не serializeb
    return JSONResponse(menu[0])


@menu_router.post("/menu",
                  status_code=status.HTTP_200_OK)
async def take_menu(token: str = Depends(get_token_iiko),
                    session_mdb:AsyncIOMotorClientSession = Depends(get_mongo_session)):
    menu = IIko()
    new_menu = await menu.take_menu(token)
    await WriteMenu(new_menu,session_mdb)
    return new_menu

