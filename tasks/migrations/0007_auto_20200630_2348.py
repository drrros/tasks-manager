# Generated by Django 3.0.7 on 2020-06-30 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_celerytask'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='celerytask',
            name='id',
        ),
        migrations.AddField(
            model_name='celerytask',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='celerytask',
            name='celery_task_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]