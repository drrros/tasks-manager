import datetime
from unittest.mock import patch

from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework import status

from .models import Task


class TestModels(TestCase):
    @patch("django.db.models.signals.ModelSignal.send", autospec=True)
    def setUp(self, mock):
        user = User.objects.create(username='user', email='user@domain.com', password='thisisnotapassword')
        Task.objects.create(
            task_header='Звонок клиенту',
            task_content='Позвонить клиенту',
            task_type='Звонок',
            task_date=timezone.localtime() + datetime.timedelta(days=4),
            author=user
        )
        self.assertTrue(mock)

    def testUserCreated(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'user')

    @patch("django.db.models.signals.ModelSignal.send", autospec=True)
    def testTasksCreated(self, mock):
        task = Task.objects.get(task_header='Звонок клиенту')
        self.assertEqual(task.task_content, 'Позвонить клиенту')
        self.assertEqual(task.task_type, 'Звонок')
        self.assertEqual(task.author, User.objects.get(id=1))
        self.assertTrue(mock)


class TestFrontend(TestCase):
    def setUp(self):
        TestModels.setUp(self)
        self.client = Client()

    @patch("django.db.models.signals.ModelSignal.send", autospec=True)
    def testHomePage(self, mock):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        response = self.client.get('/', follow=True)
        self.assertContains(response,
                            '<input type="password" name="password" placeholder="Пароль..." class="form-control" >',
                            status_code=200,
                            )
        # print(response.content.decode(encoding='utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        User.objects.create_superuser('admin', 'admin@admin.com', '123asdFGH')
        User.objects.create_user('elena', 'elena@drros.ru', 'not123asdFGH')
        self.client.post('/', data={'username': 'admin', 'password': '123asdFGH'}, follow=True)
        self.client.login(username='admin', password='123asdFGH')
        response = self.client.get('/')
        self.assertContains(response,
                            '<span class="hello-msg">Здравствуйте, admin </span>',
                            status_code=status.HTTP_200_OK,
                            html=True
                            )
        self.client.logout()
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response,
                            '<input type="password" name="password" placeholder="Пароль..." class="form-control" >',
                            status_code=status.HTTP_200_OK,
                            )
        self.client.login(username='elena', password='not123asdFGH')
        response = self.client.get('/', follow=True)
        # print(response.content.decode(encoding='utf-8'))
        self.assertContains(response,
                            '<span class="hello-msg">Здравствуйте, elena </span>',
                            status_code=status.HTTP_200_OK,
                            html=True
                            )
        response = self.client.get('/create_task', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/create_task/', data={
            'task_header': 'Тестовый звонок header',
            'task_content': 'Тестовый звонок content',
            'task_type': 'Звонок',
            'task_date': datetime.datetime.strftime(timezone.localtime()+datetime.timedelta(days=1), '%d.%m.%Y %H:%M')
        })
        print(response.content.decode(encoding='utf-8'))
        task = Task.objects.get(task_header='Тестовый звонок header')
        self.assertEqual(task.task_content, 'Тестовый звонок content')
        self.assertEqual(task.task_type, 'Звонок')
        self.assertTrue(mock)
