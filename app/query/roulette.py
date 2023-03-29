from app.db.models.models import Roulette, UserRoulette
from sqlalchemy import select, and_


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


async def get_user_won_roulettes(current_user, session):
    print("\n\n\n\n\n\n\n\n")
    user_id = current_user.id
    user_query = select(UserRoulette).where(
        and_(
            UserRoulette.user_id == user_id,
            UserRoulette.is_winner == True,
        )
    )

    user: list[UserRoulette] = await session.execute(user_query)
    user = user.scalars().all()
    if not user:
        return []

    return user
