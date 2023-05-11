from datetime import timedelta

from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.profile import Profile
from app.config import auth
from app.auth.oauth2 import get_current_user
from app.IIko import get_token_iiko
import random
from app.IIko import IIko


profile_router = APIRouter(tags=["Profile"])


@profile_router.get("/whoiam", status_code=status.HTTP_200_OK)
async def get_info_user(
    # session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
    token: str = Depends(get_token_iiko),
    sesion_iiko: IIko = Depends(IIko)
):
    resp = await sesion_iiko.get_user(current_user,token)
    return resp


@profile_router.put("/whoiam", status_code=status.HTTP_200_OK)
async def get_info_user(
    # session: AsyncSession = Depends(get_session),
    profile: Profile = Body(),
    current_user: str = Depends(get_current_user),
    token: str = Depends(get_token_iiko),
    sesion_iiko: IIko = Depends(IIko)
):
    resp = await sesion_iiko.create_or_update(token,
                                              sex=profile.sex,
                                              phone=profile.phone,
                                              name=profile.name,
                                              middleName=profile.middleName,
                                              surName=profile.surName,
                                              birthday=profile.birthday,
                                              organizationId="0915d8a9-4ca7-495f-a75c-1ce684424781",)
    return resp