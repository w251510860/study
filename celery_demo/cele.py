import time

from celery import Celery
from celery.utils.log import get_task_logger
from celery import chain
from celery import group
from celery import chord
from celery import chunks

logger = get_task_logger(__name__)
app = Celery('cele', broker='redis://localhost:6379/4', backend='redis://localhost:6379/5')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
)

app.conf.beat_schedule = {
    '10-seconds': {
        'task': 'cele.sum_a_b',
        'schedule': 3.0,
        'args': (3, 4)
    },
}


@app.task
def add(x, y):
    time.sleep(3)
    return x + y


@app.task(bind=True)
def sum_a_b(self, x, y):
    logger.info(f'self.request.id -> {self.request.id}')
    return x + y


@app.task
def sum_result(values):
    return sum(values)
