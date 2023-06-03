from celery import Celery
from datetime import timedelta, date
from app.db import models
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.config.get_settings import auth, get_settings


app = Celery("tasks", broker=auth.CELERY_BROKER_URL, backend=auth.CELERY_BACKEND_URL)
counter = 0
engine = create_engine(get_settings().database_uri)


@app.task
def create_new_roulette(*args):
    global counter, engine
    counter += 1
    with Session(engine) as session:
        new_roulette = models.Roulette(
            title=f"Рулетка №{counter}",
            start=str(date.today()),
            end=str(date.today() + timedelta(days=7)),
            score=0,
            winners_count=auth.WINNERS_COUNT
        )
        session.add(new_roulette)
        session.commit()


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'worker.commands.create_new_roulette',
        'schedule': 15.0,
    },
}
app.conf.timezone = 'UTC'
