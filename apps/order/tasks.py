from datetime import datetime

from bittrex import Bittrex, API_V1_1
from celery import app
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models import Q
from poloniex import Poloniex

from apps.order.constants import POLONIEX, BITTREX
from apps.order.models import Price, Exchange

bittrex = Bittrex('', '', api_version=API_V1_1)  # Public API


@app.shared_task()
def import_bittrex_orders_task():
    emails = User.objects.values_list('email', flat=True).distinct()
    for email in emails:
        if email:
            call_command('import_bittrex_orders', account_email=email, exchange='bittrex')


@app.shared_task()
def import_bittrex_rates_task():
    call_command('import_bittrex_rates')


@app.shared_task()
def import_bittrex_rates(pair):
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
            pair=pair, exchange=Exchange.objects.get(name=BITTREX),
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
    poloniex = Exchange.objects.get(name=POLONIEX)
    if response:
        defaults = {
            'ask': response['lowestAsk'],
            'bid': response['highestBid'],
            'timestamp': datetime.now(),
            'data': dict(response),
            'exchange_id': poloniex.id,
            'pair': pair
        }
        price, created = Price.objects.filter(
            Q(pair=pair) & Q(exchange=poloniex)
        ).get_or_create(
            defaults=defaults
        )
        if not created:
            for attr, value in defaults.items():
                setattr(price, attr, value)
            price.save()
            print('price has been updated')
        else:
            print('price has been created')
