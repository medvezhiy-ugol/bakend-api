import requests
from datetime import datetime, timedelta
from celery import Celery


def create_new_roulette(title: str):
    data = {
        'title': title,
        'start': str(datetime.now().date()),
        'end': str(datetime.now().date() + timedelta(days=7)),
        'winners_count': 0,
        'score': 100,
    }
    r = requests.post("http://94.131.97.26/v1/roulette/create", json=data)
    print(f"Создание `{title}` с параметрами:\n{data}\n")
    print(f"Результат создания: {r.json()}")
