from typing import Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_it: int


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
    code: str = Field (..., max_length=5)

class SuccessfulResponse(BaseModel):
    details: str = Field("Выполнено", title="Статус операции")


class UserInfo(BaseModel):
    name: str
    surname: str
    phone: str
    nickname: str
    role: str
