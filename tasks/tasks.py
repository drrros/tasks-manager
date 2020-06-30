import requests
import datetime
from django.utils import timezone

from celery import shared_task
from .models import Task


# celery beat --app=vz_parser_frontend.celery:app --loglevel=INFO
# celery worker --app=vz_parser_frontend.celery:app --loglevel=INFO --pool=solo


@shared_task
def send_mail(sendmail: dict):
    pass
