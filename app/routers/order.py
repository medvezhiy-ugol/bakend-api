from app.schemas.order import OrderCreate, OrderResponse, OrderResponsePydantic
from fastapi import APIRouter, status, Body, Depends
from app.IIko import get_token_iiko, IIko
from typing import List
import json
from fastapi import APIRouter, Depends, status, Body, Query, Path
from datetime import datetime
from uuid import UUID
from app.auth.oauth2 import get_current_user
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session

order_router = APIRouter(tags=["Orders"])


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
