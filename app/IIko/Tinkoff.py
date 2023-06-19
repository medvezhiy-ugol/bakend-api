from typing import List
import httpx
#from app.schemas.exception import TinkoffException
from app.config import auth
from app.schemas.order import ItemsModel, PaymentsModel
import datetime


class Tinkoff:
    def __init__(self) -> None:
        self.init_url = "https://securepay.tinkoff.ru/v2/Init"
        
        
    
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Tinkoff, cls).__new__(cls)
        return cls.instance
    
    
    async def init_tinkoff(self,order_id, Items: List[ItemsModel],discount: float):
        sum_order = sum(map(lambda item: item.amount* item.price,Items))
        data = {
            "TerminalKey": f"{auth.TINKOFF_TERMINAL}",
            "Amount": sum_order * 100 - discount *100,
            "OrderId": f"{order_id}",
            "Description": f"Заказ {order_id} в Медвежьем Угле",
            "NotificationURL": auth.URL_CONFIRM,
            "RedirectDueDate": (datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=5)).replace(microsecond=0).isoformat(),
            "Receipt": {
                "Email": "",
                "Phone": "+78005553535",
                "EmailCompany": "",
                "Payments": {
                    "Electronic": sum_order * 100 - discount *100,
                    "Provision": discount * 100
                },
                "Taxation": "usn_income",
                "Items": [ {"Name": f"Заказ №{order_id}",
                            "Price": item.price * 100,
                            "Quantity": item.amount,
                            "Amount": item.price * item.amount * 100,
                            "PaymentMethod": "full_prepayment",
                            "PaymentObject": "commodity",
                            "Tax": "none"
                            } for item in Items]
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.init_url, timeout=10.0,json=data)
            resp = response.json()
            return resp

