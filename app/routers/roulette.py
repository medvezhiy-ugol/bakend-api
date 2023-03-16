from app.schemas.roulette import RouletteInfo
from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session
from app.query.roulette import get_roulette_mongo, get_user_roulette_mongo
from fastapi.responses import JSONResponse


roulette_router = APIRouter(tags=["Roulette"])


@roulette_router.get("/roulette", status_code=status.HTTP_200_OK)
async def get_roulette(
    session_mongo: AsyncIOMotorClientSession = Depends(get_mongo_session)
    ):
    res = await get_roulette_mongo(session_mongo)
    return JSONResponse(res)


@roulette_router.get("/user_roulette", status_code=status.HTTP_200_OK)
async def get_user_roulette(
    session_mongo: AsyncIOMotorClientSession = Depends(get_mongo_session)
    ):
    res = await get_user_roulette_mongo(session_mongo)
    return JSONResponse(res)
