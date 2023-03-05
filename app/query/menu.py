from motor.motor_asyncio import AsyncIOMotorClient

async def WriteMenu(document, client:AsyncIOMotorClient):
    db = client.medvejie_ustie
    result = await db.menu.insert_one(document)
    