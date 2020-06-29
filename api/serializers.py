from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.models import Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedRelatedField(view_name='api:user-detail',
    #                                           read_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedRelatedField(view_name='api:task-detail',
    #                                           read_only=True)
    class Meta:
        model = Task
        fields = ['url', 'id', 'task_header', 'task_content', 'task_type',
                  'task_date', 'date_created', 'author']
