# Generated by Django 2.0 on 2018-06-22 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20180622_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredservice',
            name='api_key',
            field=models.CharField(blank=True, help_text='If your task endpoint requires an API key, specify it here. API key can be sent via params or Authorization Bearer', max_length=255, null=True),
        ),
    ]
