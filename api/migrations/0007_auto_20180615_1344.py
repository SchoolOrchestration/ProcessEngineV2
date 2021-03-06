# Generated by Django 2.0 on 2018-06-15 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20180614_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registeredtask',
            name='name',
        ),
        migrations.AddField(
            model_name='registeredtask',
            name='method_to_call',
            field=models.CharField(blank=True, help_text='Full path to the method to call. e.g.: `api.tasks.ping`', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='processtask',
            name='runner',
            field=models.CharField(choices=[('api.tasks.runners.http_task_runner', 'Trigger a task over HTTP')], default='api.tasks.runners.http_task_runner', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='runner',
            field=models.CharField(choices=[('api.tasks.runners.http_task_runner', 'Trigger a task over HTTP')], max_length=50),
        ),
    ]
