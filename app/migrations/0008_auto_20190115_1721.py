# Generated by Django 2.1.3 on 2019-01-15 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190115_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
