# Generated by Django 2.0 on 2018-06-14 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180613_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='This is the formal name of the test that will be called', max_length=255)),
                ('base_url', models.URLField(blank=True, help_text='The internal base url where this service can be found', null=True)),
                ('channel', models.CharField(blank=True, help_text='A channel on which this service is listening', max_length=255, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='processtask',
            name='runner',
            field=models.CharField(choices=[('api.tasks.runners.http_task_runner', 'Trigger a task over HTTP'), ('api.tasks.runners.local_task_runner', 'Call a locally available task')], default='api.tasks.runners.http_task_runner', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='runner',
            field=models.CharField(choices=[('api.tasks.runners.http_task_runner', 'Trigger a task over HTTP'), ('api.tasks.runners.local_task_runner', 'Call a locally available task')], max_length=50),
        ),
    ]
