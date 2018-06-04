# Generated by Django 2.0.5 on 2018-06-01 22:06
import os

from django.db import migrations, models
from django.core.management import call_command
import django.db.models.deletion

from apps.profile_app.models import Account


def import_bittrex_dummy_orders(apps, schema_editor):
    if os.environ.get('ENV') in ['production', 'staging', 'local']:
        for account in Account.objects.all():
            call_command('import_bittrex_orders', account_email=account.email)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('profile_app', '0001_initial'),
        ('profile_app', '0002_account_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_app.Account'),
        ),
        migrations.AddField(
            model_name='order',
            name='exchange',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Exchange'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['uuid'], name='order_order_uuid_411e74_idx'),
        ),
        migrations.RunPython(import_bittrex_dummy_orders, reverse_code=migrations.RunPython.noop),
    ]