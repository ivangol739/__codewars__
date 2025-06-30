from fastapi import BackgroundTasks, FastAPI
from celery import Celery
from tasks import call_background_task

app = FastAPI()

celery = Celery(
    __name__,
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    broker_connection_retry_on_startup=True
)


@app.get("/")
async def hello_world(message: str):
    call_background_task.apply_async(args=[message], expires=3600)
    return {"message": "Hello World"}


celery.conf.beat_schedule = {
    'run-me-background-task': {
        'task': 'tasks.call_background_task',
        'schedule': 60.0,
        'args': ('Test text message',)
    }
}