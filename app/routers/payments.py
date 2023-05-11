from datetime import timedelta

from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.profile import Profile
from app.config import auth
from app.auth.oauth2 import get_current_user
from app.IIko import get_token_iiko
import random
from app.IIko import IIko
from app.schemas.payments import Organiztion

payments_router = APIRouter(tags=["Payments"])


@payments_router.post(
    "/organization/payments",
    status_code=status.HTTP_200_OK,
)
async def get_product_from_menu(org: Organiztion = Body(...),
                                token: str = Depends(get_token_iiko),
                                sesion_iiko: IIko = Depends(IIko)):
    return await sesion_iiko.payments_org(org.org,token)

@payments_router.post(
    "/order/payments",
    status_code=status.HTTP_200_OK,
)
async def get_product_from_menu(org: Organiztion = Body(...),
                                token: str = Depends(get_token_iiko),
                                sesion_iiko: IIko = Depends(IIko)):
    return await sesion_iiko.order_payments(org.org,token)