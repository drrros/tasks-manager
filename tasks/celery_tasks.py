import smtplib

from celery import shared_task
from django.core.mail import send_mail

from .models import CeleryTask


# celery worker --app=tasks_manager.celery:app --loglevel=DEBUG --pool=solo
# celery purge -f --app=tasks_manager.celery:app


@shared_task
def sendemail(recipient: str, task_header: str, task_content: str, task_date: str, task_type: str):
    """Send notification email."""
    try:
        # https://github.com/celery/celery/issues/4300
        celery_task = CeleryTask.objects.get(celery_task_id=sendemail.request.id)
        if not celery_task.completed:
            print('task: sendemail, recepient:' + recipient)
            try:
                send_mail(
                    f'Напоминание о событии: {task_header}',
                    f'Событие {task_header} ({task_content}) - {task_type} начнётся через 1 час в {task_date}',
                    'notify@domain.ru',
                    [recipient, ],
                    fail_silently=False,
                )
            except smtplib.SMTPException as e:
                print(e)
                # TODO: make smth with it (retry?)
            celery_task.completed = True
            celery_task.save()
            return True
        return False
    except CeleryTask.DoesNotExist:
        return False
