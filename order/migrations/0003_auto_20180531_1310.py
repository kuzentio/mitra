# Generated by Django 2.0.5 on 2018-05-31 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20180525_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='name',
            field=models.CharField(choices=[('bittrex', 'Bittrex'), ('binance', 'Binance'), ('bitfinex', 'Bitfinex'), ('bitfinex', 'Bitfinex'), ('okcoin', 'Okcoin')], max_length=255, unique=True),
        ),
    ]
