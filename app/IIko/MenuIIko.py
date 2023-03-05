import httpx
from app.schemas.exception import IIkoServerExeption
from os import environ
from dotenv import load_dotenv
import asyncio
load_dotenv("local.env")


class MenuIIko:


    async def take_menu(self,token: str) :
        url_iiko: str =  environ.get("IIKO_MENU")
        data = {
                "organizationIds": ["df66facb-ba7e-4752-be86-afc034dbeaa5"],
                "externalMenuId": "9583"
        }
        headers = headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url_iiko,
                                         json=data, timeout=10.0,headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp
