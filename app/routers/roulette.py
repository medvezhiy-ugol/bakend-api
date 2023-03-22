from fastapi import APIRouter, status, Depends, Form
from app.query.roulette import get_all_roulettes, create_roulette
from app.schemas.roulette import RouletteInfo
from app.db.connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Page
from datetime import date
from fastapi.responses import JSONResponse
from app.schemas.auth import SuccessfulResponse


roulette_router = APIRouter(tags=["Roulette"])


@roulette_router.get(
    '/roulette/all',
    status_code=status.HTTP_200_OK,
    response_model=Page[RouletteInfo]
)
async def get_roulettes(session: AsyncSession = Depends(get_session)):
    query_get_roulettes = await get_all_roulettes()
    return await paginate(session, query_get_roulettes)


@roulette_router.post('/roulette/create', status_code=status.HTTP_200_OK)
async def add_new_roulette(
    title: str = Form(
        ...,
        description="Roulette title",
        min_length=3,
        max_length=999,
    ),
    start: date = Form(
        ...,
        description="Roulette start (YYYY-MM-DD)"
    ),
    end: date = Form(
        ...,
        description="Roulette end (YYYY-MM-DD)"
    ),
    score: int = Form(
        ...,
        description="Roulette score",
        lt=1000,
    ),
    winners_count: int = Form(
        ...,
        description="Roulette winners count",
        lt=1000,
    ),
    session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    await create_roulette(title, start, end, score, winners_count, session)
    return SuccessfulResponse()
