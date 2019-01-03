from datetime import datetime

from bittrex import Bittrex, API_V1_1
from celery import app
from django.contrib.auth.models import User
from django.core.management import call_command
from poloniex import Poloniex

from apps.order.constants import EXCHANGES_CHOICES
from apps.order.models import Price, Exchange

bittrex = Bittrex('', '', api_version=API_V1_1)  # Public API


@app.shared_task()
def import_bittrex_orders_task():
    emails = User.objects.values_list('email', flat=True).distinct()
    for email in emails:
        if email:
            call_command('import_bittrex_orders', account_email=email, exchange='bittrex')


@app.shared_task()
def import_bittrex_prices_task():
    call_command('import_bittrex_prices')


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
            pair=pair, exchange=Exchange.objects.get(name=EXCHANGES_CHOICES[0][0]),
            defaults=defaults
        )
        if not created:
            for attr, value in defaults.items():
                setattr(price, attr, value)
            price.save()
            print('price has been updated')
        else:
            print('price has been created')


@app.shared_task()
def import_poloniex_orders_task():
    emails = User.objects.values_list('email', flat=True).distinct()
    for email in emails:
        if email:
            call_command('import_poloniex_orders', account_email=email, exchange='poloniex')


@app.shared_task()
def import_poloniex_rates_task():
    call_command('import_poloniex_rates')


@app.shared_task()
def import_poloniex_rates(pair):
    poloniex = Poloniex()
    _pair = '_'.join(pair.split('-'))
    response = poloniex.returnTicker()[_pair]
    if response:
        defaults = {
            'ask': response['lowestAsk'],
            'bid': response['highestBid'],
            'timestamp': datetime.now(),
            'data': dict(response)
        }
        price, created = Price.objects.get_or_create(
            pair=pair, exchange=Exchange.objects.get(name=EXCHANGES_CHOICES[1][0]),
            defaults=defaults
        )
        if not created:
            for attr, value in defaults.items():
                setattr(price, attr, value)
            price.save()
            print('price has been updated')
        else:
            print('price has been created')
