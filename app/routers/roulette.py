from fastapi import APIRouter, status, Depends, Form, Body
from app.query.roulette import get_all_roulettes, create_roulette
from app.schemas.roulette import RouletteInfo, RouletteCreateForm
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
    user = await session.scalar(query_get_roulettes)

    print("\n\n\n\n\n\n\n", user, "\n\n\n\n\n\n")

    result = await paginate(session, query_get_roulettes)
    
    return result


@roulette_router.post('/roulette/create', status_code=status.HTTP_200_OK)
async def add_new_roulette(
    data: RouletteCreateForm = Body(...),
    session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    await create_roulette(
        data.title,
        data.start,
        data.end,
        data.score,
        data.winners_count,
        session
    )
    return SuccessfulResponse()


@roulette_router.get('/roulette/accept_roulette/')
async def accept_roulette_by_id():
    pass