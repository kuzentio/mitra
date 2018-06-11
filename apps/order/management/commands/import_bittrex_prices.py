import os

from bittrex import Bittrex, API_V1_1
from django.core.management import BaseCommand

from apps.order import tasks
from apps.order.models import Order


bittrex = Bittrex('', '', api_version=API_V1_1)  # Public API


class Command(BaseCommand):
    help = 'Import prices from Bittrex and store it into db.'

    def handle(self, *args, **options):
        all_pairs = Order.objects.all().values_list('pair', flat=True).distinct()
        for pair in all_pairs:
            if os.environ.get('ENV') in ['local', 'test', None]:
                tasks.import_bittrex_price(pair)

            tasks.import_bittrex_price.apply_async((pair,))
        self.stdout.write('Done')
