# Generated by Django 2.0.5 on 2018-08-13 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='bid',
            field=models.DecimalField(decimal_places=8, default=0.0, max_digits=12),
            preserve_default=False,
        ),
    ]
