import datetime

from django.conf import settings
from django.db import models

class Task(models.Model):
    task_type_choice = [
        ('Встреча', 'Встреча'),
        ('Звонок', 'Звонок')
    ]
    task_header = models.CharField(max_length=100, null=False, blank=False)
    task_content = models.CharField(max_length=1000, null=True, blank=True)
    task_type = models.CharField(choices=task_type_choice, max_length=30, null=False, blank=False)
    task_date = models.DateTimeField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task_header} ({self.task_type})'

    @property
    def recent(self):
        return self.date_created > (self.date_created - datetime.timedelta(days=1))