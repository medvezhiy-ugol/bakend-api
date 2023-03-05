from fastapi import APIRouter, Depends, status, Body
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session
from app.IIko import get_token_iiko,MenuIIko
from app.query.menu import WriteMenu
from app.db.connection import get_mongo_session


menu_router = APIRouter(tags=["Menu"])


@menu_router.get("/menu",
    status_code=status.HTTP_200_OK)
async def get_menu(session_mongo: AsyncIOMotorClientSession = Depends(get_mongo_session)):
    pass

@menu_router.post("/menu",
                  status_code=status.HTTP_200_OK)
async def take_menu(token: str = Depends(get_token_iiko),
                    session_mdb:AsyncIOMotorClientSession = Depends(get_mongo_session)):
    menu = MenuIIko()
    new_menu = await menu.take_menu(token)
    await WriteMenu(new_menu,session_mdb)
    return new_menu
