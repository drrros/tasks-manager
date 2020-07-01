from celery import shared_task

from .models import CeleryTask


# celery worker --app=tasks_manager.celery:app --loglevel=DEBUG --pool=solo
# celery purge -f --app=tasks_manager.celery:app


@shared_task
def sendemail(recipient):
    try:
        celery_task = CeleryTask.objects.get(celery_task_id=sendemail.request.id)
        if not celery_task.completed:
            print('task: sendemail, recepient:' + recipient)
            # send_mail(
            #     'Subject here',
            #     'Here is the message.',
            #     'from@example.com',
            #     [recipient,],
            #     fail_silently=False,
            # )
            celery_task.completed = True
            celery_task.save()
            return True
        return False
    except CeleryTask.DoesNotExist:
        return False
