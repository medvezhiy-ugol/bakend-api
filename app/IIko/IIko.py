import httpx
from app.schemas.exception import IIkoServerExeption
from typing import Dict, Optional
from app.schemas.terminal import TerminalModel
from enum import Enum


class chequeAdditionalInfoView(Enum):
    needReceipt: Optional[bool]
    email: Optional[str]
    settlementPlace: Optional[str]
    phone: Optional[str]


class IIko:
    def __init__(self) -> None:
        self.url_base = "https://api-ru.iiko.services/"
        self.url_menu = "api/2/menu/by_id"
        self.url_orgs = "api/1/reserve/available_organizations"
        self.url_term = "api/1/terminal_groups"
        self.url_order = "api/1/order/create"
        self.url_menu_id = "api/2/menu"
        self.url_combo = "api/1/combo"
        self.url_sms = "api/1/loyalty/iiko/message/send_sms"
        self.url_create_customer = "api/1/loyalty/iiko/customer/create_or_update"
        self.url_whoiam = "api/1/loyalty/iiko/customer/info"
        self.url_payments_types = "api/1/payment_types"
        self.url_order_types = "api/1/deliveries/order_types"
        self.url_close_order = "api/1/order/close"

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(IIko, cls).__new__(cls)
        return cls.instance
    
    async def auth_phone(self, phone: str):
        url = self.url_auth_phone
        data = {
            "from": "MedveshUgol",
            "text": f"Activate code:",
            "to": phone,
            "api_key": ""
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, timeout=10.0,data=data)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp

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
            "organizationIds": ["0915d8a9-4ca7-495f-a75c-1ce684424781"],
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
        data = {
                "organizationIds": [],
                "returnAdditionalInfo": True,
                "includeDisabled": True
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=10.0, headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp

    async def get_combos_iiko(self, token: str, organizationId: str ):
        url = self.url_base + self.url_combo
        data = {
            "extraData": True,
            "organizationId": organizationId
            }   
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json=data, timeout=10.0, headers=headers
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
                url, json=data, timeout=10.0, headers=headers
            )
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp
    
    async def create_or_update(
            self,
            token: str,
            sex: int,
            organizationId: str,
            phone: str = None,
            cardTrack: str = None,
            cardNumber: str = None,
            name: str = None,
            middleName: str = None,
            surName: str = None,
            birthday: str = None,
            ):
        url = self.url_base + self.url_create_customer
        data = {
            "phone": phone,
            "name": name,
            "middleName": middleName,
            "surName": surName,
            "birthday": birthday,
            "sex": sex,
            "organizationId": organizationId,
        }
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json=data, timeout=10.0, headers=headers
            )
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp

    async def get_user(self, phone: str, token: str):
        url = self.url_base + self.url_whoiam
        data = {
            "phone": phone,
            "type": "phone",
            "organizationId": "0915d8a9-4ca7-495f-a75c-1ce684424781"
        }
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json=data, timeout=10.0, headers=headers
            )
            if "There is no user with phone" in response.text:
                return None
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp
        
    async def reg_user( self,
                        token: str,
                        organizationId: str,
                        phone: str,
                        name: str,
                        ):
        url = self.url_base + self.url_create_customer
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "phone": phone,
            "name": name,
            "organizationId": organizationId,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json=data, timeout=10.0, headers=headers
            )
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp
    
    async def payments_org(self,org: str, token: str):
        url = self.url_base + self.url_payments_types
        data = {
            "organizationIds": [f"{org}"],
        }
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=10.0, headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp
        
    async def order_payments(self, org: str, token: str):
        url = self.url_base + self.url_order_types
        data = {
            "organizationIds": [f"{org}"],
        }
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=10.0, headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp

    async def close_order(
            self,
            token: str,
            organizationId: str,
            orderId: str,
            chequeAdditionalInfo: chequeAdditionalInfoView = None
            ):
        url = self.url_base + self.url_close_order
        data = {
            "organizationId": organizationId,
            "orderId": orderId,
        }
        if chequeAdditionalInfo:
            data.setdefault("chequeAdditionalInfo", {
                "needReceipt": None,
                "email": None,
                "settlementPlace": None,
                "phone": None
            })
            if chequeAdditionalInfo.needReceipt:
                data['chequeAdditionalInfo']['needReceipt'] = chequeAdditionalInfo.needReceipt
            if chequeAdditionalInfo.email:
                data['chequeAdditionalInfo']['email'] = chequeAdditionalInfo.email
            if chequeAdditionalInfo.settlementPlace:
                data['chequeAdditionalInfo']['settlementPlace'] = chequeAdditionalInfo.settlementPlace
            if chequeAdditionalInfo.phone:
                data['chequeAdditionalInfo']['phone'] = chequeAdditionalInfo.phone

        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=10.0, headers=headers)
            if response.status_code != 200:
                raise IIkoServerExeption(error=response.text)
            resp = response.json()
            return resp
