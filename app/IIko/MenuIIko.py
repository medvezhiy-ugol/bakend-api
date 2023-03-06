import httpx
from app.schemas.exception import IIkoServerExeption
from typing import Dict
from app.config import DefaultSettings


class IIko:

    def __init__(self) -> None:
        settings = DefaultSettings()
        self.url_base = settings.URL_BASE
        self.url_menu = settings.URL_MENU
        self.url_token = settings.URL_TOKEN
        self.url_orgs = settings.URL_ORGANIZATIONS
        self.url_term = settings.URL_TERMINAL


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IIko, cls).__new__(cls)
        return cls.instance
    
    
    async def take_menu(self, token: str, **data: Dict) -> Dict:
        url = self.url_base + self.take_menu
        data = {
                "organizationIds": ["df66facb-ba7e-4752-be86-afc034dbeaa5"],
                "externalMenuId": "9583"
        }
        headers = headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url,
                                         json=data, timeout=10.0,headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp


    async def take_terminal(self, token: str, **data: Dict) -> Dict:
        url = self.url_base + self.take_terminal
        data = {
                "organizationIds": ["df66facb-ba7e-4752-be86-afc034dbeaa5"],
                "includeDisabled": True
        }
        headers = headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url,
                                         json=data, timeout=10.0,headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp
    
    async def create_order(self, token: str, **data: Dict)-> Dict:
        url = self.url_base + self.create_order
        headers = headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url,
                                         json=data, timeout=10.0,headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
                #TODO может сделат ьсериализацию и отправку??
            resp = response.json()
            return resp

    
    async def get_organiztions(self, token: str) -> Dict:
        url = self.url_base + self.url_orgs
        headers = headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0,headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp
