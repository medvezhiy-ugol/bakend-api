from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class RouletteInfo(BaseModel):
    id: UUID
    title: str
    start: datetime
    end: datetime
    score: int
    winners_count: int


class UserRouletteInfo(BaseModel):
    id: UUID
    user_id: UUID
    roulette_id: UUID
    is_winner: bool
