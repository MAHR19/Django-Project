# Generated by Django 3.2.12 on 2022-08-15 21:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_userprofileinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 15, 21, 18, 59, 41602, tzinfo=utc)),
        ),
    ]
