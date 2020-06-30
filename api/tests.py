import datetime

from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from tasks.models import Task
from .serializers import UserSerializer, TaskSerializer


class TasksTest(APITestCase):
    """ Test module for test tasks API """

    def setUp(self):
        user = User.objects.create(username='user', email='user@domain.com', password='thisisnotapassword')
        user2 = User.objects.create(username='user2', email='user2@domain.com', password='2thisisnotapassword')
        Task.objects.create(
            task_header='Task header user',
            task_content='Task content user',
            task_type='Звонок',
            task_date=timezone.localtime() + datetime.timedelta(days=4),
            author=user
        )
        admin = User.objects.create_superuser(username='admin', email='admin@drros.ru', password='123AdminPassword')
        Task.objects.create(
            task_header='Task header admin',
            task_content='Task content admin',
            task_type='Звонок',
            task_date=timezone.localtime() + datetime.timedelta(days=3),
            author=admin
        )

        # self.client = APIClient()

    def testTasks(self):
        # test unauthenticated response
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticate using token
        user = User.objects.get(username='user')
        user_token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
        # self.client.force_authenticate(user=user)

        # test authenticated response
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test task serializing
        response = self.client.get(reverse('task-list'))
        context = {'request': RequestFactory().get(reverse('task-list'))}
        tasks = Task.objects.filter(author_id=user.id)
        serialized_tasks = TaskSerializer(tasks, many=True, context=context)
        self.assertEqual(response.data, serialized_tasks.data)

        # test create task
        response_create = self.client.post(reverse('task-list'), data={
            'task_header': 'Task header user 2',
            'task_content': 'Task content user',
            'task_type': 'Звонок',
            'task_date': timezone.localtime() + datetime.timedelta(days=4)
        })
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('task-list'))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response_create.data['id'], response.data[1]['id'])
        self.client.force_authenticate(user=None)

        # test admin can access user's tasks
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        response = self.client.get(reverse('task-detail', kwargs={'pk': response_create.data['id']}))
        self.assertEqual(response.data, response_create.data)

        # test user can't access other users tasks
        self.client.force_authenticate(user=None)
        user2 = User.objects.get(username='user2')
        user2_token = Token.objects.create(user=user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user2_token.key)
        response = self.client.get(reverse('task-detail', kwargs={'pk': response_create.data['id']}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserTest(APITestCase):
    """ Test module for test users API """

    def setUp(self):
        User.objects.create_superuser(username='admin', email='admin@drros.ru', password='123AdminPassword')

    def testUsers(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.client.force_authenticate(user=User.objects.get(username='admin'))

        # authenticate using token
        admin = User.objects.get(username='admin')
        admin_token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)

        # test authenticated response
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test admin can access self.details
        response = self.client.get(reverse('user-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test user serializing
        response = self.client.get(reverse('user-list'))
        context = {'request': RequestFactory().get(reverse('user-list'))}
        users = User.objects.all()
        serialized_users = UserSerializer(users, many=True, context=context)
        self.assertEqual(response.data, serialized_users.data)

        # test user creation
        data = {
            'username': 'user123',
            'email': 'user@user.com',
            'password': '123UserPassword'
        }
        response_create = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        # test user can't create other users
        user123 = User.objects.get(username='user123')
        self.client.force_authenticate(user=user123)
        data2 = {
            'username': 'user123',
            'email': 'user@user.com',
            'password': '123UserPassword'
        }
        response_create2 = self.client.post(reverse('user-list'), data2, format='json')
        self.assertEqual(response_create2.status_code, status.HTTP_403_FORBIDDEN)

        # test user can access self.details
        response = self.client.get(reverse('user-detail', kwargs={'pk': response_create.data['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test user can't access other details
        response = self.client.get(reverse('user-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # test user can't update self.details
        response = self.client.put(reverse('user-detail', kwargs={'pk': response_create.data['id']}),
                                   data={'email': 'user321@user321.ru'}
                                   )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
