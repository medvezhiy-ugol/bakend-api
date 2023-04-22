import httpx
from app.schemas.exception import IIkoServerExeption
from typing import Dict
from app.schemas.terminal import TerminalModel


class IIko:
    def __init__(self) -> None:
        self.url_base = "https://api-ru.iiko.services/"
        self.url_menu = "api/2/menu/by_id"
        self.url_orgs = "api/1/organizations"
        self.url_term = "api/1/terminal_groups"
        self.url_order = "api/1/order/create"
        self.url_menu_id = "api/2/menu"
        self.url_combo = "api/1/combo"
        self.url_sms = "api/1/loyalty/iiko/message/send_sms"
        self.url_create_customer = "api/1/loyalty/iiko/customer/create_or_update"

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(IIko, cls).__new__(cls)
        return cls.instance

    async def take_info_menu(self, token: str) -> Dict:
        url = self.url_base + self.url_menu_id
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, timeout=10.0, headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp

    async def take_menu_byid(self, token: str, data: int) -> Dict:
        url = self.url_base + self.url_menu
        data = {
            "organizationIds": ["df66facb-ba7e-4752-be86-afc034dbeaa5"],
            "externalMenuId": str(data),
        }
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=10.0, headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp

    async def take_terminal(self, token: str, data: TerminalModel) -> Dict:
        url = self.url_base + self.url_term
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json=data.json(), timeout=10.0, headers=headers
            )
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp

    async def create_order(self, token: str, **data: Dict) -> Dict:
        url = self.url_base + self.url_order
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=10.0, headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
                # TODO может сделат ьсериализацию и отправку??
            resp = response.json()
            return resp

    async def get_organiztions(self, token: str) -> Dict:
        url = self.url_base + self.url_orgs
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0, headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp

    async def get_combos_iiko(self, token: str, organizationId: str):
        url = self.url_base + self.url_combo
        data = {
            "extraData": True,
            "organizationId": organizationId
            }
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json=data.json(), timeout=10.0, headers=headers
            )
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp

    async def send_sms(self, token: str, phone: str, text: str, organizationId: str):
        url = self.url_base + self.url_sms
        data = {
            "phone": phone,
            "text": text,
            "organizationId": organizationId,
        }
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json=data.json(), timeout=10.0, headers=headers
            )
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp

    async def create_or_update(
            self,
            token: str,
            sex: int,
            consentStatus: int,
            organizationId: str,
            id: str = None,
            phone: str = None,
            cardTrack: str = None,
            cardNumber: str = None,
            name: str = None,
            middleName: str = None,
            surName: str = None,
            birthday: str = None,
            email: str = None,
            shouldReceivePromoActionsInfo: bool = None,
            referrerId: str = None,
            userData: str = None,
            ):
        url = self.url_base + self.url_create_customer
        data = {
            "id": id,
            "phone": phone,
            "cardTrack": cardTrack,
            "cardNumber": cardNumber,
            "name": name,
            "middleName": middleName,
            "surName": surName,
            "birthday": birthday,
            "email": email,
            "sex": sex,
            "consentStatus": consentStatus,
            "shouldReceivePromoActionsInfo": shouldReceivePromoActionsInfo,
            "referrerId": referrerId,
            "userData": userData,
            "organizationId": organizationId,
        }
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json=data.json(), timeout=10.0, headers=headers
            )
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp
