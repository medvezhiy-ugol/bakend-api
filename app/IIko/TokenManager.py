import httpx
import requests
from time import perf_counter
from app.schemas.exception import IIkoServerExeption
import asyncio
from app.config import DefaultSettings


class TokenManager:
    """
    Создает токен, с периодичностью в часы
    """

    def __init__(self) -> None:
        self.time_create = perf_counter()
        settings = DefaultSettings()
        self.url_iiko = "https://api-ru.iiko.services/"
        self.url_token = "api/1/access_token"
        self.api_login = settings.API_LOGIN
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(TokenManager, cls).__new__(cls)
        return cls.instance

    def get_token(self):
        if perf_counter() - self.time_create >= 40 * 10000:
            self.refresh()
        return self.token

    def refresh(self) -> None:
            response = requests.post(
                self.url_iiko + self.url_token,
                json={"apiLogin": self.api_login},
                timeout=10.0,
            )
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            self.token = resp["token"]


def get_token_iiko() -> str:
    session_maker = TokenManager()
    return session_maker.get_token()
