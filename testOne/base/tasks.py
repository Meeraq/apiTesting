import string
from celery import shared_task


@shared_task
def add(a, b):
    print(a + b)
