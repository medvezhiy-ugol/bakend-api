from fastapi import APIRouter, status, Depends, Form, Body
from app.query.roulette import get_all_roulettes, create_roulette, get_user_won_roulettes
from app.schemas.roulette import RouletteInfo, RouletteCreateForm, UserRouletteInfo
from app.db.connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Page
from datetime import date
from fastapi.responses import JSONResponse
from app.schemas.auth import SuccessfulResponse
from app.auth.oauth2 import get_current_user
from app.query.auth import find_by_nickname
from app.utils import serialize_models

roulette_router = APIRouter(tags=["Roulette"])


@roulette_router.get(
    '/roulette/all',
    status_code=status.HTTP_200_OK,
    response_model=Page[RouletteInfo]
)
async def get_roulettes(session: AsyncSession = Depends(get_session)):
    query_get_roulettes = await get_all_roulettes()
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


@roulette_router.get('/roulette/user_won_roulette/', response_model=list[UserRouletteInfo], status_code=status.HTTP_200_OK)
async def won_user_roulettes(
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    result = await find_by_nickname(current_user, session)
    answer = await get_user_won_roulettes(result, session)
    return serialize_models(answer, UserRouletteInfo)
