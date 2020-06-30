from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.models import Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(view_name='task-detail',
                                                many=True,
                                                read_only=True
                                                # queryset=Task.objects.all()
                                                )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'password', 'tasks']


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Task
        fields = ['url', 'id', 'task_header', 'task_content', 'task_type',
                  'task_date', 'date_created', 'author']
