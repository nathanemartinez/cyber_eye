from celery import shared_task
from time import sleep
from django.core.mail import send_mail

@shared_task
def add(x, y):
    return x + y


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_mail_task():
    send_mail('celery task worked', 'yeet', 'seonathanm@gmail.com', ['nathanemtz@gmail.com'])
    return None
