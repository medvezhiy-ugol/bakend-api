from app.db.models.models import Roulette, UserRoulette
from sqlalchemy import select, and_, update
import random
from app.IIko import get_token_iiko, IIko
from app.config import auth
from fastapi import Depends
from typing import List


async def get_all_roulettes():
    querry_join = (
        select(
           Roulette.id.label("id"),
           Roulette.title.label("title"),
           Roulette.start.label("start"),
           Roulette.end.label("end"),
           Roulette.score.label("score"),
           Roulette.winners_count.label("winners_count"),
        )
    )
    return querry_join


async def create_roulette(title, start, end, score, winners_count, session):
    new_roulette = Roulette(
        title=title, start=start, end=end, score=score, winners_count=winners_count
    )
    session.add(new_roulette)
    await session.commit()


async def add_user_to_roulette(user_id,user_phone: str, wallet_id: str, sum: int, organization_id: str, session):
    roulettes: list[Roulette] = await session.execute(select(Roulette))
    roulette = roulettes.scalars().all()[-1]
    this_user_in_roulette = (await session.execute(
        select(UserRoulette).where(
            (UserRoulette.roulette_id == roulette.id) & (UserRoulette.user_id == user_id)
        )
    )).scalars().first()

    if not this_user_in_roulette:
        user_in_roulette = UserRoulette(
            user_id=user_phone,
            roulette_id=str(roulette.id),
            wallet_id=str(wallet_id),
            organization_id=str(user_id)
        )
        session.add(user_in_roulette)
        await session.commit()

    user_query = update(Roulette).where((Roulette.id == roulette.id)).values(score=roulette.score + sum)
    await session.execute(user_query)
    await session.commit()

async def get_last_roulette_async(session):
    roulettes: list[Roulette] = await session.execute(select(Roulette))
    roulette: Roulette = roulettes.scalars().all()[-1]
    return roulette

def get_last_roulette(session):
    roulettes: list[Roulette] = session.execute(select(Roulette))
    roulette: Roulette = roulettes.scalars().all()[-1]
    return roulette

async def get_winners_by_roulette_id(session, roulette_id):
    query = select(UserRoulette).where(
        (UserRoulette.roulette_id == roulette_id) & (UserRoulette.is_winner == True)
    )
    winners: list[UserRoulette] = (await session.execute(query)).scalars().all()
    return winners


def get_random_winner(session):
    roulette = get_last_roulette(session)
    query = select(UserRoulette).where(UserRoulette.roulette_id == roulette.id)
    all_users_in_roulette = (session.execute(query)).scalars().all()
    try:
        winners = random.sample(all_users_in_roulette, roulette.winners_count)
    except:
        winners = [random.choice(all_users_in_roulette)]
    return winners


async def process_winner(session, users: List[UserRoulette], sum, winners_count, sesion_iiko: IIko, token):
    winning_money = sum / winners_count
    for winner in users:
        query = update(UserRoulette).where(UserRoulette.id == winner.id).values(is_winner=True)
        session.execute(query)
        await sesion_iiko.change_balance(
            token, winner.wallet_id, winner.organization_id, winning_money, "0915d8a9-4ca7-495f-a75c-1ce684424781"
        )

    # вызвать из commands.py функцию create_new_roulette или автоматически создавать в селери
