from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from app.config import auth
from app.schemas.auth import RefreshTokenView, TokenType
from app.query.auth import decode_token
from app.schemas.exception import DoNotUsuRefreshToken


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, auth.SECRET_KEY, algorithm=auth.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> str:
    token: RefreshTokenView = decode_token(token)
    if token.token_type_access == TokenType.REFRESH:
        raise DoNotUsuRefreshToken
    return token.sub
