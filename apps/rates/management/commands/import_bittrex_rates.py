from datetime import datetime
from decimal import Decimal

from bittrex import Bittrex, API_V2_0
from django.core.management import BaseCommand

from apps.order.models import Exchange
from apps.rates.constants import BITTREX_RATES_MAPPING
from apps.rates.models import BTCRate


class Command(BaseCommand):
    def get_rate_defaults(self, rate):
        result = {}
        field_mapping = dict(BITTREX_RATES_MAPPING)
        for key, value in rate.items():
            if key not in field_mapping.keys():
                continue
            if type(value) in [int, float]:
                value = Decimal(str(value))
            if field_mapping[key] not in ['-', '', None]:
                result[field_mapping[key]] = value
            if field_mapping[key] == 'datetime':
                result[field_mapping[key]] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

        return result

    def handle(self, *args, **options):
        bittrex = Bittrex(
            api_key=None,  # This is open api resource so we no need credentials
            api_secret=None,
            api_version=API_V2_0
        )
        response = bittrex.get_candles(
            market='USDT-BTC',
            tick_interval='hour',
        )
        if not response.get('success') is True:
            self.stdout.write('Wrong response  {}'.format(response))
        rates = response.get('result')
        if rates is None:
            self.stdout.write('Could not find rates in {}'.format(response))
            return
        count = 0
        for rate in rates:
            defaults = self.get_rate_defaults(rate)
            defaults['exchange'] = Exchange.objects.get(name='bittrex')
            defaults['data'] = rate
            rate, created = BTCRate.objects.get_or_create(
                exchange=defaults['exchange'],
                datetime=defaults['datetime'],
                defaults=defaults
            )
            if created:
                count += 1
        self.stdout.write('Total rates were created - {}'.format(count))
        return