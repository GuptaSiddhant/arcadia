# Generated by Django 2.1.3 on 2019-01-22 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20190122_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamescore',
            name='playedDate',
        ),
        migrations.RemoveField(
            model_name='gamestate',
            name='savedDate',
        ),
        migrations.AddField(
            model_name='gamescore',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='gamestate',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
