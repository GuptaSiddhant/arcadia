# Generated by Django 2.1.3 on 2019-01-22 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20190122_2038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamescore',
            old_name='play_date',
            new_name='playedDate',
        ),
        migrations.RenameField(
            model_name='gamestate',
            old_name='save_date',
            new_name='savedDate',
        ),
    ]
