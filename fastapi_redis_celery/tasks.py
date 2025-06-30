from celery import shared_task
import time


@shared_task()
def call_background_task(message):
    time.sleep(10)
    print(f"Background Task called!")
    print(message)
