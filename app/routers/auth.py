from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session
from app.schemas.auth import Token, AuthUser, AuthUserCode, SuccessfulResponse, RefreshTokenView, Settings, TokenType
from app.config import auth
from app.query.auth import generate_tokens, decode_token
from app.IIko import get_token_iiko
from app.db.connection import Redis
from app.schemas.exception import IncorrectCodeException, TimeOutCodeException, NoRefreshToken
import random
from app.IIko import IIko
from fastapi_jwt_auth import AuthJWT
from app.config.default import settings_just

registr_router = APIRouter(tags=["Authorization"])


@AuthJWT.load_config
def get_config():
    return Settings()


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
    code = str(random.randint(1000, 9999))
    if phone.phone != settings_just.APPLE_PHONE:
        await redis.set_code_phone(phone=phone.phone, code=code)
        await sesion_iiko.send_sms(token_iiko, phone.phone, code, "0915d8a9-4ca7-495f-a75c-1ce684424781")
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
    if creds.phone != settings_just.APPLE_PHONE:
        check = await redis.get_code_phone(phone=creds.phone)
        if check is None:
            raise TimeOutCodeException(error="Время истекло")
        if check != creds.code:
            raise IncorrectCodeException(error="Код не верен")
    resp = await sesion_iiko.get_user(creds.phone, token)
    if resp is None:
        code_for_name_user = str(random.randint(1, 9999999))
        await sesion_iiko.reg_user(token, "0915d8a9-4ca7-495f-a75c-1ce684424781", creds.phone,
                                   f"user{code_for_name_user}")
    tokens = generate_tokens(sub=creds.phone)
    return Token(access_token=tokens["access_token"],
                 refresh_token=tokens["refresh_token"],
                 token_type="Bearer",
                 token_type_access="Access/Refresh",
                 expires_it=auth.ACCESS_TOKEN_EXPIRE_MINUTES)


@registr_router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    token: RefreshTokenView = decode_token(Authorize._token)

    if token.token_type_access == TokenType.ACCESS:
        raise NoRefreshToken

    data: dict = generate_tokens(sub=token.sub)
    return Token(access_token=data["access_token"],
                 refresh_token=data["refresh_token"],
                 token_type="Bearer",
                 token_type_access="Access/Refresh",
                 expires_it=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
