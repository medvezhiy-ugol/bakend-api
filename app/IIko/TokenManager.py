import httpx
from time import perf_counter
from app.schemas.exception import IIkoServerExeption
import asyncio
from app.config import DefaultSettings


class TokenManager:
    """
    Создает токен, с периодичностью в часЫ
    """

    def __init__(self) -> None:
        self.time_create = perf_counter()
        settings = DefaultSettings()
        self.url_iiko = 'https://api-ru.iiko.services/'
        self.url_token = 'api/1/access_token'
        self.api_login = settings.API_LOGIN
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.refresh())


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TokenManager, cls).__new__(cls)
        return cls.instance

    
    def get_token(self):
        if perf_counter() - self.time_create >= 10:
            self.loop.run_until_complete(self.refresh())
        return self.token
    
    
    async def refresh(self) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.post(self.url_iiko + self.url_token,json= {"apiLogin": self.api_login }, timeout=10.0)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            self.token = resp['token']

def get_token_iiko() -> str:
    session_maker = TokenManager()
    return session_maker.get_token()