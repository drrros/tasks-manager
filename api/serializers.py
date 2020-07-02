from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.models import Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(view_name='task-detail',
                                                many=True,
                                                read_only=True
                                                # queryset=Task.objects.all()
                                                )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'password', 'tasks']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        user = super(UserSerializer, self).update(instance, validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class TaskSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Task
        fields = ['url', 'id', 'task_header', 'task_content', 'task_type',
                  'task_date', 'date_created', 'author']
