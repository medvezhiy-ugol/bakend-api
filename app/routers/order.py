from app.schemas.order import OrderCreate, OrderResponse, OrderResponsePydantic
from fastapi import APIRouter, status, Body, Depends
from app.IIko import get_token_iiko, IIko
import json
from datetime import datetime
from uuid import UUID
from app.auth.oauth2 import get_current_user
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session

order_router = APIRouter(tags=["Orders"])

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


@order_router.post("/create", status_code=status.HTTP_200_OK)
async def create_new_order(
    session_mdb: AsyncIOMotorClientSession = Depends(get_mongo_session),
    Order: OrderCreate = Body(...),
    token: str = Depends(get_token_iiko),
    sesion_iiko: IIko = Depends(IIko),
    current_user: str = Depends(get_current_user),
):

    Order.order.phone = current_user
    Order.order.customer.birthdate = datetime.now()
    response = await sesion_iiko.create_order(token, data=Order)

    await OrderResponse(**response, user_id=current_user, id=response['orderInfo']['id']).save()
    return response


# get_history_by_user_id + paginate