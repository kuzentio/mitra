# Generated by Django 2.0.5 on 2018-08-13 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0003_herokucredentials'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='legal',
            name='user',
        ),
        migrations.DeleteModel(
            name='Legal',
        ),
    ]
