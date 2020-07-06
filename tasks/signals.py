import datetime

from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import Task, CeleryTask
from .celery_tasks import sendemail


@receiver(post_save, sender=Task)
def tasks_post_save_signal(sender, instance: Task, **kwargs):
    """Post save Task signal"""
    # new task
    eta = instance.task_date - datetime.timedelta(hours=1)
    expires = eta + datetime.timedelta(minutes=40)
    celery_task = sendemail.apply_async((instance.author.email,
                                         instance.task_header,
                                         instance.task_content,
                                         instance.task_date,
                                         instance.task_type), eta=eta, expires=expires)
    CeleryTask.objects.create(celery_task_id=celery_task.id,
                              corresp_task=instance,
                              completed=False)


@receiver(pre_save, sender=Task)
def tasks_pre_save_signal(sender, instance: Task, **kwargs):
    """Pre save Task signal"""
    try:
        celery_task = CeleryTask.objects.get(corresp_task=instance)
        celery_task.delete()
    except CeleryTask.DoesNotExist:
        pass


@receiver(pre_delete, sender=Task)
def tasks_pre_delete_signal(sender, instance: Task, **kwargs):
    """Pre delete Task signal"""
    try:
        celery_task = CeleryTask.objects.get(corresp_task=instance)
        celery_task.delete()
    except CeleryTask.DoesNotExist:
        pass
