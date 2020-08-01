# Generated by Django 3.0.3 on 2020-07-22 11:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200722_0446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='create_date',
        ),
        migrations.AddField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 22, 11, 47, 38, 455362, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 22, 11, 47, 38, 459360, tzinfo=utc)),
        ),
    ]