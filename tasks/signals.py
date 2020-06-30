from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task
from .tasks import send_mail



@receiver(pre_save, sender=Task)
def order_signal(sender, instance: Task, **kwargs):
       pass
