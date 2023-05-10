from datetime import timedelta

from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session
from app.schemas.auth import Token, RegUser, AuthUser, UserInfo,AuthUserCode, SuccessfulResponse
from app.config import auth
from app.auth.jwttoken import create_access_token
from app.query.auth import check_nickname, create_user, find_by_nickname, get_info
from app.auth.oauth2 import get_current_user
from app.IIko import get_token_iiko
from app.db.connection import Redis
from app.schemas.exception import IncorrectCodeException, TimeOutCodeException
import random
from app.IIko import IIko
from fastapi_jwt_auth import AuthJWT


registr_router = APIRouter(tags=["Authorization"])


@registr_router.post(
    "/login",
    response_model=SuccessfulResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    phone: AuthUser = Body(...), 
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(Redis),
    sesion_iiko: IIko = Depends(IIko),
    token_iiko: str = Depends(get_token_iiko),
) -> SuccessfulResponse:
    code = str(random.randint(1000,9999))
    await redis.set_code_phone(phone=phone.phone,code=code)
    await sesion_iiko.send_sms(token_iiko,phone.phone,code,"0915d8a9-4ca7-495f-a75c-1ce684424781")
    return SuccessfulResponse()


@registr_router.post(
    "/check/code",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={status.HTTP_401_UNAUTHORIZED: {"detail": "Код не верен"},
               status.HTTP_403_FORBIDDEN: {"detail": "Время истекло"}
               },
)
async def verify_phone(creds: AuthUserCode = Body(),
                       redis: Redis = Depends(Redis),
                       Authorize: AuthJWT = Depends(),
                       sesion_iiko: IIko = Depends(IIko),
                       token: str = Depends(get_token_iiko)):
    
    check = await redis.get_code_phone(phone=creds.phone)
    if check is None:
        raise TimeOutCodeException(error="Время истекло")
    if check != creds.code:
        raise IncorrectCodeException(error="Код не верен")
    resp = await sesion_iiko.get_user(creds.phone,token)
    if resp is None:
        code_for_name_user = str(random.randint(1,9999999))
        await sesion_iiko.reg_user(token,"0915d8a9-4ca7-495f-a75c-1ce684424781",creds.phone,
                               f"user{code_for_name_user}")
    
    refresh_token = Authorize.create_refresh_token(subject=creds.phone,algorithm="HS384")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
       data={"sub": creds.phone}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, 
                 token_type="Bearer",
                 refresh_token=refresh_token, 
                 expires_it=auth.ACCESS_TOKEN_EXPIRE_MINUTES)


@registr_router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
       data={"sub": current_user}, expires_delta=access_token_expires
    )
    refresh_token = Authorize.create_refresh_token(subject=current_user,algorithm="HS384")
    return Token(access_token=access_token, 
                 token_type="Bearer",
                 refresh_token=refresh_token,
                 expires_it=auth.ACCESS_TOKEN_EXPIRE_MINUTES)

