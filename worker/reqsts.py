import requests
from datetime import datetime, timedelta
from celery import Celery
from app.db import models
from sqlalchemy import select
from app.db.connection import get_session


async def create_new_roulette(title: str):
    new_roulette = models.Roulette(
        title=title,
        start=str(datetime.now().date()),
        end=str(datetime.now().date() + timedelta(days=7)),
        score=0,
        winners_count=100
    )
    session = get_session()
    session.add(new_roulette)

    print(f"Создание `{title}` с параметрами:")
    print(f"Начало: {str(datetime.now().date())}")
    print(f"Конец: {str(datetime.now().date() + timedelta(days=7))}\n")
