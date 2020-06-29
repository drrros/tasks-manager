from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.models import Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(view_name='task-detail',
                                                many=True,
                                                read_only=True
                                                # queryset=Task.objects.all()
                                                )

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'tasks']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(view_name='user-detail',
                                                 # read_only=True
                                                 queryset=User.objects.all()
                                                 )

    class Meta:
        model = Task
        fields = ['url', 'id', 'task_header', 'task_content', 'task_type',
                  'task_date', 'date_created', 'author']
