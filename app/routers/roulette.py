from fastapi import APIRouter, status, Depends
from app.query.roulette import get_all_roulettes
from app.schemas.roulette import RouletteInfo
from app.db.connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Page


roulette_router = APIRouter(tags=["Roulette"])


@roulette_router.get(
    '/roulette/all',
    status_code=status.HTTP_200_OK,
    response_model=Page[RouletteInfo]
)
async def get_roulettes(session: AsyncSession = Depends(get_session)):
    query_get_roulettes = await get_all_roulettes()
    return await paginate(session, query_get_roulettes)
