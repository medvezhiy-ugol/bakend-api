from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session
from app.IIko import get_token_iiko, IIko
from app.query.menu import write_to_mongo,get_menu_mongo
from app.db.connection import get_mongo_session
from app.schemas.menu import MenuCredits


menu_router = APIRouter(tags=["Menu"])



@menu_router.get("/menu")
async def get_menu_id(token: str = Depends(get_token_iiko),
                      sesion_iiko: IIko = Depends(IIko)):
    resp = await sesion_iiko.take_info_menu(token)
    return resp
    
@menu_router.post("/menu/by_id",
    status_code=status.HTTP_200_OK)
async def get_menu(menu_org : MenuCredits = Body(...),
                   session_mongo: AsyncIOMotorClientSession = Depends(get_mongo_session)):
    menu = await get_menu_mongo(menu_org, session_mongo)
    #menu[0].pop("_id") # УДаляю ObjectID так как он не serializeb
    return JSONResponse(menu)


@menu_router.post("/menu/iiko/by_id",
                  status_code=status.HTTP_200_OK)
async def take_menu(token: str = Depends(get_token_iiko),
                    session_mdb:AsyncIOMotorClientSession = Depends(get_mongo_session),
                    sesion_iiko: IIko = Depends(IIko)):
    new_menu = await sesion_iiko.take_menu_byid(token)
    await write_to_mongo(new_menu,session_mdb)
    return new_menu

