# Generated by Django 2.1.3 on 2019-01-22 20:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20190122_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamescore',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 22, 20, 46, 56, 395239, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='gamestate',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 22, 20, 46, 56, 394674, tzinfo=utc)),
        ),
    ]
