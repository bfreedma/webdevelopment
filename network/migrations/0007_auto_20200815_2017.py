# Generated by Django 3.0.8 on 2020-08-16 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20200815_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='following_count',
            field=models.IntegerField(default=0),
        ),
    ]
