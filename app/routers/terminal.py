from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session
from app.IIko import get_token_iiko, IIko
from app.query.menu import WriteMenu,get_menu_mongo
from app.db.connection import get_mongo_session



terminal_router = APIRouter(tags=["Terminal"])


@terminal_router.get("/terminal",
    status_code=status.HTTP_200_OK)
async def get_all_terminals(token: str = Depends(get_token_iiko)):
    terminals = await IIko().take_terminal(token)
    return terminals


@terminal_router.post("/terminal",
                  status_code=status.HTTP_200_OK)
async def take_menu(token: str = Depends(get_token_iiko),
                    session_mdb:AsyncIOMotorClientSession = Depends(get_mongo_session)):
    menu = IIko()
    new_menu = await menu.take_menu(token)
    await WriteMenu(new_menu,session_mdb)
    return new_menu
