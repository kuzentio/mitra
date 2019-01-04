from decimal import Decimal

from poloniex import Poloniex, PoloniexCommandException
from django.core.management import BaseCommand, CommandError

from apps.order.constants import EXCHANGES_CHOICES, POLONIEX_ORDER_MAPPING
from apps.order.models import Order, Exchange
from apps.profile_app.models import Account


class Command(BaseCommand):
    help = 'Import orders from poloniex exchange.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--account_email',
            type=str,
            action='store',
            dest='email',
            default=None,
            help='Account email.'
        )
        parser.add_argument(
            '--exchange',
            type=str,
            action='store',
            dest='exchange',
            default=None,
            help='Exchange name, for example: "bittrex".'
        )

    def get_order_defaults(self, order):
        result = {}
        field_mapping = dict(POLONIEX_ORDER_MAPPING)
        for key, value in order.items():
            if key not in field_mapping.keys():
                continue
            if field_mapping[key] not in ['-', '', None]:
                result[field_mapping[key]] = value
            if field_mapping[key] == 'type':
                result[field_mapping[key]] = value.upper()
        result['price'] = Decimal(order['total']) / Decimal(order['amount'])
        result['commission'] = result['price'] * Decimal(order['amount']) / Decimal('1000')
        result['closed_at'] = order['date']

        return result

    def save_orders(self, account, orders, pair):
        for order in orders:
            uuid = order.get('orderNumber')

            defaults = self.get_order_defaults(order)
            defaults['exchange_id'] = Exchange.objects.get(name=EXCHANGES_CHOICES[1][0]).id
            defaults['pair'] = pair
            order, created = Order.objects.get_or_create(
                uuid=uuid,
                account=account,
                defaults=defaults
            )
            if created:
                self.stdout.write(f'Order {order.pk} has been created.')

    def handle(self, *args, **options):
        email = options.get('email')
        exchange = options.get('exchange')
        if not email:
            raise CommandError(
                "Please provide --account_email. See details --help"
            )
        accounts = Account.objects.filter(
            user__email=email,
            exchange__name=exchange,
            is_active=True
        )
        if not accounts.exists():
            raise CommandError(
                f"Could not find account for {exchange} with {email} email"
            )
        for account in accounts:
            api_key = account.api_key
            api_secret = account.api_secret

            polo = Poloniex(
                api_key, api_secret
            )
            try:
                history = polo.returnTradeHistory()
            except PoloniexCommandException as e:
                self.stdout.write(f'Poloniex connection problem. {e}')
            for pair in list(history):
                orders = history[pair]
                pair = '-'.join(pair.split('_'))

                self.save_orders(account, orders, pair)
            self.stdout.write('Done.')
