from bittrex import Bittrex, API_V1_1
from django.core.management import BaseCommand

from apps.order import tasks
from apps.order.models import Order


bittrex = Bittrex('', '', api_version=API_V1_1)  # Public API


class Command(BaseCommand):
    help = 'Import prices from Poloniex and store it into db.'

    def handle(self, *args, **options):
        orders = Order.objects.filter(exchange__name='poloniex')
        if not orders.exists():
            self.stdout.write('There is no orders')
            return
        all_pairs = orders.values_list('pair', flat=True).distinct()
        for pair in all_pairs:
            tasks.import_poloniex_rates(pair)
        self.stdout.write('Done')
