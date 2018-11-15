from datetime import datetime

from bittrex import Bittrex, API_V1_1
from celery import shared_task, app
from django.contrib.auth.models import User
from django.core.management import call_command

from apps.order import constants
from apps.order.models import Price


bittrex = Bittrex('', '', api_version=API_V1_1)  # Public API


@shared_task(bind=True)
def import_bittrex_orders_task(self):
    # emails = Account.objects.all().values_list('user__email', flat=True)
    emails = User.objects.values_list('email', flat=True).distinct()
    for exchange, _ in constants.EXCHANGES_CHOICES:
        for email in emails:
            if email:
                call_command('import_bittrex_orders', account_email=email, exchange=exchange)


@app.shared_task()
def import_bittrex_price(pair):
    response = bittrex.get_ticker(pair)
    result = response['result']
    if result:  # TODO: install Logger (!)
        defaults = {
            'ask': result['Ask'],
            'bid': result['Bid'],
            'timestamp': datetime.now(),
            'data': result,
        }
        price, created = Price.objects.get_or_create(
            pair=pair,
            defaults=defaults
        )
        if not created:
            for attr, value in defaults.items():
                setattr(price, attr, value)
            price.save()
            print('price has been updated')  # TODO: smell code (!)
        else:
            print('price has been created')
