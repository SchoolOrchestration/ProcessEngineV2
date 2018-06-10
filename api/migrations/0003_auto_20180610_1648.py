# Generated by Django 2.0 on 2018-06-10 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180606_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredtask',
            name='friendly_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='registeredtask',
            name='name',
            field=models.CharField(blank=True, help_text='This is the formal name of the test that will be called', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='registeredtask',
            name='service',
            field=models.CharField(blank=True, help_text='This is downstream service to call', max_length=255, null=True),
        ),
    ]
