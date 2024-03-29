from pydantic import BaseModel
from uuid import UUID
from datetime import date


class RouletteInfo(BaseModel):
    id: UUID
    title: str
    start: date
    end: date
    score: int
    winners_count: int

    class Config:
        orm_mode = True


class RouletteWinner(BaseModel):
    user_id: str
    wallet_id: UUID

    class Config:
        orm_mode = True


class UserRouletteInfo(BaseModel):
    id: UUID
    user_id: UUID
    roulette_id: UUID
    is_winner: bool

    class Config:
        orm_mode = True


class RouletteCreateForm(BaseModel):
    title: str
    start: date
    end: date
    score: int
    winners_count: int
