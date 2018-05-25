from bittrex import Bittrex, API_V2_0, API_V1_1
from django.core.management import BaseCommand, CommandError

from order.constance import BITTREX_ORDER_MAPPING, EXCHANGES_CHOICES
from order.models import Order, Exchange
from profile_app.models import Account


class Command(BaseCommand):
    help = 'Import orders from bittrex remote, and save into DB if not exists'

    def add_arguments(self, parser):
        parser.add_argument(
            '--account_email',
            type=str,
            action='store',
            dest='email',
            default=None,
            help='Account email.'
        )

    def get_order_defaults(self, order):
        result = {}
        field_mapping = dict(BITTREX_ORDER_MAPPING)
        for key, value in order.items():
            if key not in field_mapping.keys():
                continue
            if field_mapping[key] not in ['-', '', None]:
                result[field_mapping[key]] = value
            if field_mapping[key] == 'type':
                result[field_mapping[key]] = value.split('_')[-1]
        return result

    def save_orders(self, account, orders):
        for order in orders:
            uuid = order.get('OrderUuid')

            defaults = self.get_order_defaults(order)
            defaults['exchange_id'] = Exchange.objects.get(name=EXCHANGES_CHOICES[0][0]).id
            order, created = Order.objects.get_or_create(
                uuid=uuid,
                account=account,
                defaults=defaults
            )
            if created:
                self.stdout.write('Order {} has been created.'.format(order.pk))

        return

    def handle(self, *args, **options):
        email = options.get('email')
        if not email:
            raise CommandError(
                "Please provide -account_email. See details --help"
            )
        account = Account.objects.filter(user__email=email, is_active=True)
        if not account.exists():
            raise CommandError(
                "Could not find account with {} email".format(email)
            )
        account = account.get()
        if not all([account.api_key, account.api_secret]):
            raise CommandError(
                "Wrong account, check that API_KEY and API_SECRET were provided."
            )

        bittrex = Bittrex(
            account.api_key, account.api_secret,
            # api_version=API_V2_0
            api_version=API_V1_1
        )
        response = bittrex.get_order_history()
        orders = response.get('result')
        if orders is None:
            self.stdout.write('There no new orders: API response - {}'.format(response))
            return
        self.save_orders(account, orders)
        self.stdout.write('Done')
        return


