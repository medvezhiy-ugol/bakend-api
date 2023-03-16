from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, List
from app.schemas.roulette import RouletteInfo, UserRouletteInfo


async def get_roulette_mongo(client: AsyncIOMotorClient):
    roulettes = client.medvejie_ustie.RouletteInfo
    return await roulettes.find().to_list(length=None)


async def get_user_roulette_mongo(client: AsyncIOMotorClient):
    roulettes = client.medvejie_ustie.UserRouletteInfo
    return await roulettes.find().to_list(length=None)