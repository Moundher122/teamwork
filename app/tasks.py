from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def test_task():
    print("!!! Celery is working! Task executed successfully !!!")
    return "Success"