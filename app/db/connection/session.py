from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from app.config import get_settings
from typing import Any, AsyncGenerator
import redis.asyncio as redis


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def refresh(self) -> None:
        self.engine = create_async_engine(
            get_settings().database_uri_async, echo=True, future=True
        )


async def get_session() -> AsyncSession:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session


class MongoManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def get_async_client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(get_settings().database_mongo)


async def get_mongo_session() -> AsyncGenerator[AsyncIOMotorClientSession, None]:
    """Get an `AsyncIOMotorClientSession` for transaction operation.

    This always creates a new client and ends the session on exit. If the
    the transaction was not committed it is aborted.
    """
    client = MongoManager().get_async_client()
    try:
        pong = await client.admin.command("ping")
        if not pong.get("ok"):
            raise
        yield client
    finally:
        client.close()


class Redis:

    con: redis.Redis = None
    
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Redis, cls).__new__(cls)
        return cls.instance 
    
    @classmethod
    async def connect_redis(cls) -> None:
        cls.con = None
        cls.con = redis.from_url(
                get_settings().REDIS_URL,
                encoding="utf-8", decode_responses=True)
    
    @classmethod
    async def disconnect_redis(cls) -> None:
        if cls.con:
            await cls.con.close()

    async def set_code_phone(self, phone: str, code: str) -> None:
        await self.con.set(phone, code)
        await self.con.expire(phone,5* 60)
        
    async def get_code_phone(self, phone) -> str:
        return await self.con.get(phone)
    

__all__ = ["get_session", "get_mongo_session"]
