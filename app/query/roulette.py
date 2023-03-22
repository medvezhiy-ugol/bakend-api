from app.db.models.models import Roulette
from sqlalchemy import select


async def get_all_roulettes():
    querry_join = (
        select(
            Roulette.id,
            Roulette.title,
            Roulette.start,
            Roulette.end,
            Roulette.score,
            Roulette.winners_count
        )
    )
    return querry_join


async def create_roulette(title, start, end, score, winners_count, session):
    new_roulette = Roulette(
        title=title, start=start, end=end, score=score, winners_count=winners_count
    )
    session.add(new_roulette)
    await session.commit()
