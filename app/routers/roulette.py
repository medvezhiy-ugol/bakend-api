from fastapi import APIRouter, status, Depends, Form, Body, Path
import app.query.roulette as ruletki
from app.schemas.roulette import RouletteInfo, RouletteCreateForm, UserRouletteInfo, RouletteWinner
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
from app.db.models import Roulette, UserRoulette
from app.IIko import get_token_iiko, IIko

from typing import List

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

@roulette_router.get("/roulette/{roulette_id}/winners", response_model=List[RouletteWinner])
async def get_winners_by_roulette_id(
    roulette_id: str = Path(...),
    session: AsyncSession = Depends(get_session),
    ):
    result = await ruletki.get_winners_by_roulette_id(session, roulette_id)
    return result
    
@roulette_router.get('/roulette/win')
async def get_winner(
    session: AsyncSession = Depends(get_session),
    sesion_iiko: IIko = Depends(IIko),
    token: str = Depends(get_token_iiko)
):
    winners = await ruletki.get_random_winner(session)
    roulette = await ruletki.get_last_roulette(session)
    await ruletki.process_winner(
        users=winners,
        sum=roulette.score,
        winners_count=roulette.winners_count,
        sesion_iiko=sesion_iiko,
        token=token,
        session=session
    )

    return SuccessfulResponse()
