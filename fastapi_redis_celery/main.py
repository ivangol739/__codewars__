from fastapi import BackgroundTasks, FastAPI
from celery import Celery

import time


app = FastAPI()

celery = Celery(
    __name__,
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    broker_connection_retry_on_startup=True
)

@celery.task()
def call_background_task(message):
    time.sleep(10)
    print(f"Background Task called!")
    print(message)


@app.get("/")
async def hello_world(message: str):
    call_background_task.delay(message)
    return {"message": "Hello World"}