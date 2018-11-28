# Generated by Django 2.0.5 on 2018-11-24 22:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0002_auto_20180810_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='port',
            field=models.PositiveIntegerField(default=7000, unique=True, validators=[django.core.validators.MinValueValidator(7000), django.core.validators.MaxValueValidator(7500)]),
            preserve_default=False,
        ),
    ]