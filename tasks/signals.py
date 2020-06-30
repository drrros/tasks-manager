import datetime

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Task, CeleryTask
from .celery_tasks import sendemail


@receiver(post_save, sender=Task)
def tasks_post_save_signal(sender, instance: Task, **kwargs):
    # new task
    eta = instance.task_date - datetime.timedelta(hours=1)
    expires = eta + datetime.timedelta(minutes=40)
    celery_task = sendemail.apply_async((instance.author.email,), eta=eta, expires=expires)
    CeleryTask.objects.create(celery_task_id=celery_task.id,
                              corresp_task=instance,
                              completed=False)
    pass


@receiver(pre_save, sender=Task)
def tasks_pre_save_signal(sender, instance: Task, **kwargs):
    try:
        celery_task = CeleryTask.objects.get(corresp_task=instance)
        celery_task.delete()
    except CeleryTask.DoesNotExist:
        pass
