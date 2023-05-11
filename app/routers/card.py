from datetime import timedelta

from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.profile import Profile
from app.config import auth
from app.auth.oauth2 import get_current_user
from app.IIko import get_token_iiko
import random
from app.IIko import IIko


card_router = APIRouter(tags=["Card"])