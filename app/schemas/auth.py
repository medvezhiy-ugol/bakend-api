from typing import Optional
from enum import StrEnum
from pydantic import BaseModel, Field
from app.config import DefaultSettings
import uuid


class Settings(BaseModel):
    authjwt_secret_key: str = DefaultSettings().JWT_SECRET
    authjwt_algorithm: str = DefaultSettings().JWT_ALG


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    token_type_access: str
    expires_it: int


class TokenType(StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class AccessTokenView(BaseModel):
    iss: str = DefaultSettings().APP_NAME
    sub: str | uuid.UUID
    exp: int
    token_type_access: str


class RefreshTokenView(BaseModel):
    iss: str = DefaultSettings().APP_NAME
    sub: str | uuid.UUID
    exp: int
    token_type_access: str


class TokenData(BaseModel):
    login: Optional[str] = None


class RegUser(BaseModel):
    name: str
    phone: str
    code: str


class AuthUser(BaseModel):
    phone: str = Field(..., max_length=30)


class AuthUserCode(BaseModel):
    phone: str = Field(..., max_length=30)
    code: str = Field(..., max_length=5)


class SuccessfulResponse(BaseModel):
    details: str = Field("Выполнено", title="Статус операции")


class UserInfo(BaseModel):
    name: str
    surname: str
    phone: str
    nickname: str
    role: str
