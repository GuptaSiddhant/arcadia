# Generated by Django 2.1.3 on 2019-01-09 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_dev',
            field=models.BooleanField(default=False),
        ),
    ]
