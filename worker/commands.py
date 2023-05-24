from celery import Celery
from datetime import datetime, timedelta
from app.db import models
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")
counter = 0


@app.task
def create_new_roulette(*args):
    global counter
    counter += 1
    engine = create_engine("postgresql://postgres:postgres@localhost:6432/medvezhiy-ugol")
    with Session(engine) as session:
        new_roulette = models.Roulette(
            title=f"Рулетка №{counter}",
            start=str(datetime.now().date()),
            end=str(datetime.now().date() + timedelta(days=7)),
            score=0,
            winners_count=100
        )
        session.add(new_roulette)
        session.commit()
    counter += 1


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'worker.commands.create_new_roulette',
        'schedule': 15.0,
    },
}
app.conf.timezone = 'UTC'
