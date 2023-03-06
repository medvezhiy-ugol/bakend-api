import httpx
from app.schemas.exception import IIkoServerExeption
from typing import Dict
from app.config import DefaultSettings


class IIko:

    def __init__(self) -> None:
        self.url_base = 'https://api-ru.iiko.services/'
        self.url_menu = 'api/2/menu/by_id'
        self.url_orgs = 'api/1/organizations'
        self.url_term = 'api/1/terminal_groups'
        self.url_order = 'api/1/order/create'


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IIko, cls).__new__(cls)
        return cls.instance
    
    
    async def take_menu(self, token: str, **data: Dict) -> Dict:
        url = self.url_base + self.url_menu
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
        url = self.url_base + self.url_term
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
        url = self.url_base + self.url_order
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
