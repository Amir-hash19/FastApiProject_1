from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",  
)

celery_app.conf.update(
    result_backend="redis://redis:6379/0"
)


@celery_app.task
def add(x, y):
    return x + y
