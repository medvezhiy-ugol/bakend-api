from app.schemas.order import OrderCreate, OrderResponse, OrderResponsePydantic, OrderCreateDraft, TinkoffRequest
from fastapi import APIRouter, status, Body, Depends
from app.IIko import get_token_iiko, IIko
from typing import List
from app.db.connection import Redis
import json
from fastapi import APIRouter, Depends, status, Body, Query, Path
from datetime import datetime
from uuid import UUID
from app.auth.oauth2 import get_current_user
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session
from uuid import uuid4
from app.IIko.Tinkoff import Tinkoff
from app.schemas.exception import BadRequest
import json
from copy import deepcopy

order_router = APIRouter(tags=["Orders"])


@order_router.post("/confirm", status_code=status.HTTP_200_OK)
async def create_order(
    tinkoff: TinkoffRequest = Body(...),
    token: str = Depends(get_token_iiko),
    sesion_iiko: IIko = Depends(IIko),
    redis: Redis = Depends(Redis)
):

    data = await redis.con.get(tinkoff.OrderId)
    if not tinkoff.Success:
        raise BadRequest(error="Заказ не принят")
    order = OrderCreate(**json.loads(data))
    user_phone = order.order.phone
    
    resp = await sesion_iiko.get_user(user_phone, token)
    payment = next(filter(lambda payment: payment.paymentTypeKind == "IikoCard",order.order.payments), None)
    if payment is None:
        discount = 0
    else:
        discount = deepcopy(payment.sum)
        del(order.order.payments[1])
        resp = await sesion_iiko.change_balance(token,resp["walletBalances"][0]["id"],resp["id"],discount,order.organizationId,False)
    response = await sesion_iiko.create_order(token, data=order)
    await OrderResponse(**response, user_id=user_phone,id=response['orderInfo']['id']).save()
    return response


@order_router.post("/create", status_code=status.HTTP_200_OK)
async def create_new_order(
    order: OrderCreate = Body(...),
    token: str = Depends(get_token_iiko),
    sesion_iiko: IIko = Depends(IIko),
    current_user: str = Depends(get_current_user),
    redis: Redis = Depends(Redis),
    tinkoff: Tinkoff = Depends(Tinkoff)
):
    uuid_order = uuid4()
    order.order.phone = current_user
    order.order.id=uuid_order
    resp = await sesion_iiko.get_user(current_user, token)
    balance = resp["walletBalances"][0]["balance"]
    payment = next(filter(lambda payment: payment.paymentTypeKind == "IikoCard",order.order.payments), None)
    if payment is not None:
        if balance < payment.sum:
            raise BadRequest(error="Баланс карты меньше заявленной суммы")
        discount = payment.sum
    else:
        discount = 0
    await redis.con.set(str(uuid_order),order.json(),ex=1800)
    response = await tinkoff.init_tinkoff(uuid_order,order.order.items,discount=0)
    return response

@order_router.get(
    "/get_history/{skip}/{limit}",
    status_code=status.HTTP_200_OK,
    response_model=List[OrderResponse],
    response_model_exclude={"_id"},
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Продуктов в категории не найден"}},
)
async def get_history_by_user(
    current_user: str = Depends(get_current_user),
    skip: int = Path(...),
    limit: int = Path(...),
):
    menu_product = await OrderResponse.find(
        OrderResponse.user_id == current_user,
        skip=skip,
        limit=limit,
        fetch_links=True
    ).to_list()
    return menu_product
