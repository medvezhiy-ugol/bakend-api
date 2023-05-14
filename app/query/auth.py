from sqlalchemy import select
from app.db.models import Users
from app.schemas.auth import RegUser, UserInfo, AccessTokenView, TokenType, RefreshTokenView
from app.schemas.exception import UserFoundException, NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.config import auth
from app.config import DefaultSettings
import jwt
from app.schemas.exception import IncorrectCodeException
import time
from pydantic import ValidationError


def get_exp_time(token_type: TokenType) -> int:
    now = datetime.now()

    if token_type == TokenType.ACCESS:
        now += timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    if token_type == TokenType.REFRESH:
        now += timedelta(days=30)

    return int(now.timestamp())


def encode_jwt(payload: AccessTokenView | RefreshTokenView):
    return jwt.encode(payload.dict(), DefaultSettings().JWT_SECRET, algorithm=DefaultSettings().JWT_ALG)


def generate_tokens(sub: str) -> dict:
    access_token_view = AccessTokenView(
        sub=sub,
        exp=get_exp_time(token_type=TokenType.ACCESS),
        token_type_access=TokenType.ACCESS
    )
    refresh_token_view = RefreshTokenView(
        sub=sub,
        exp=get_exp_time(TokenType.REFRESH),
        token_type_access=TokenType.REFRESH
    )
    access_token = encode_jwt(access_token_view)
    refresh_token = encode_jwt(refresh_token_view)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "exp": access_token_view.exp,
    }


def decode_token(token: str) -> RefreshTokenView:
    if type(token) != str:
        token = token.credentials

    try:
        payload = jwt.decode(
            token, DefaultSettings().JWT_SECRET, algorithms=[DefaultSettings().JWT_ALG],
            options={"verify_signature": True}
        )
        if not payload:
            raise IncorrectCodeException
        
        token_data = RefreshTokenView(**payload)
        if time.time() > token_data.exp:
            raise IncorrectCodeException
    except (jwt.DecodeError, jwt.ExpiredSignatureError, ValidationError) as e:
        raise IncorrectCodeException(error=str(e))
    return token_data


async def check_nickname(nickname: str, session: AsyncSession):
    user_query = select(Users).where(Users.nickname == nickname)
    user: Users = await session.scalar(user_query)
    if user:
        raise UserFoundException(error="Юзер с таким nickname существует")


async def create_user(new_user: RegUser, session: AsyncSession):
    new_user = Users(
        nickname=new_user.nickname,
        name=new_user.name,
        surname=new_user.surname,
        user_type="User",
        phone=new_user.phone,
    )
    session.add(new_user)
    await session.commit()


async def find_by_nickname(nickname: str, session: AsyncSession) -> str:
    user_query = select(Users).where(Users.nickname == nickname)
    user: Users = await session.scalar(user_query)
    if not user:
        raise NotFoundException(error="Пользователь не найден")
    return user


async def get_info(nickname: str, session: AsyncSession):
    user_query = select(Users).where(Users.nickname == nickname)
    user: Users = await session.scalar(user_query)
    userOut = UserInfo(
        name=user.name,
        surname=user.surname,
        nickname=user.nickname,
        phone=user.phone,
        role=user.user_type,
    )
    return userOut
