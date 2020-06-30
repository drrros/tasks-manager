from celery import shared_task

from .models import CeleryTask


# celery beat --app=tasks_manager.celery:app --loglevel=DEBUG
# celery worker --app=tasks_manager.celery:app --loglevel=DEBUG --pool=solo


@shared_task
def sendemail(recipient):
    try:
        celery_task = CeleryTask.objects.get(celery_task_id=sendemail.request.id)
        print('task: sendemail, recepient:' + recipient)
        celery_task.completed = True
        celery_task.save()
        # send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     'from@example.com',
        #     [recipient,],
        #     fail_silently=False,
        # )
        return True

    except CeleryTask.DoesNotExist:
        return False