import smtplib

from celery import shared_task
from django.core.mail import send_mail

from .models import CeleryTask


# celery worker --app=tasks_manager.celery:app --loglevel=DEBUG --pool=solo
# celery purge -f --app=tasks_manager.celery:app


@shared_task
def sendemail(recipient, task_header, task_content, task_date, task_type):
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
                    [recipient,],
                    fail_silently=False,
                )
            except smtplib.SMTPException as e:
                pass
                # TODO: make smth with it (retry?)
            celery_task.completed = True
            celery_task.save()
            return True
        return False
    except CeleryTask.DoesNotExist:
        return False
