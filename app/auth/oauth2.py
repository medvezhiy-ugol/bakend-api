from fastapi import Depends
from fastapi.security import HTTPBearer

from app.auth.jwttoken import verify_token

oauth2_scheme = HTTPBearer()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    return verify_token(token)
