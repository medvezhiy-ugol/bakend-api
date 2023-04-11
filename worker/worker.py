import os, time
from celery import Celery
from reqsts import create_new_roulette

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_roulette(roulette_counter: int) -> int:
    create_new_roulette(f"Рулетка №{roulette_counter}")
    time.sleep(604800)  # 7 days
