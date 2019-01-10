# Generated by Django 2.1.3 on 2019-01-10 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20190106_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='icon',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.URLField(blank=True, default='/static/media/no-image.png'),
        ),
    ]
