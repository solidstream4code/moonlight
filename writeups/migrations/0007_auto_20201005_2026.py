# Generated by Django 3.0.5 on 2020-10-06 03:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('writeups', '0006_auto_20201004_2226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='writeup',
            name='date',
        ),
        migrations.AddField(
            model_name='writeup',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]