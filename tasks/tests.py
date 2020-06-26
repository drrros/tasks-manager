import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Task


class TestModels(TestCase):
    def setUp(self):
        user = User.objects.create(username='user', email='user@domain.com', password='thisisnotapassword')
        Task.objects.create(
            task_header='Звонок клиенту',
            task_content='Позвонить клиенту',
            task_type='Звонок',
            task_date=timezone.localtime() + datetime.timedelta(days=4),
            author=user
        )

    def testUserCreated(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'user')

    def testTaksCreated(self):
        task = Task.objects.get(task_header='Звонок клиенту')
        self.assertEqual(task.task_content, 'Позвонить клиенту')
        self.assertEqual(task.task_type, 'Звонок')
        self.assertEqual(task.author, User.objects.get(id=1))
