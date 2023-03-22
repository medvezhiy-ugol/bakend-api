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
