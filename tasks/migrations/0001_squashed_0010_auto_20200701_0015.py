# Generated by Django 3.0.7 on 2020-07-01 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    replaces = [('tasks', '0001_initial'), ('tasks', '0002_auto_20200627_0122'), ('tasks', '0003_auto_20200628_2312'), ('tasks', '0004_auto_20200629_1450'), ('tasks', '0005_auto_20200629_2139'), ('tasks', '0006_celerytask'), ('tasks', '0007_auto_20200630_2348'), ('tasks', '0008_auto_20200701_0000'), ('tasks', '0009_auto_20200701_0011'), ('tasks', '0010_auto_20200701_0015')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('task_header', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('task_content', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Описание события')),
                ('task_type', models.CharField(choices=[('Встреча', 'Встреча'), ('Звонок', 'Звонок')], max_length=30, verbose_name='Тип события')),
                ('task_date', models.DateTimeField(verbose_name='Дата события')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CeleryTask',
            fields=[
                ('celery_task_id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('corresp_task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='celery_task', to='tasks.Task')),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]
