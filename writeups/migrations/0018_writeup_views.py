# Generated by Django 3.0.5 on 2020-10-13 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writeups', '0017_auto_20201012_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='writeup',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
