import csv

import sys

from datetime import datetime
from decimal import Decimal
from django.core.management import BaseCommand, CommandError
from django.utils.timezone import get_current_timezone

from order.constance import BITTREX_ORDER_MAPPING
from order.models import Order

tz = get_current_timezone()


class Command(BaseCommand):
    help = 'Upload Bittrex orders in CSV format'
    total_orders_created = 0

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def _get_ordered_mapping(self, row):
        ordered_items_mapping = []
        for _field in row:
            field = dict(BITTREX_ORDER_MAPPING).get(_field)
            if field is not None:
                ordered_items_mapping.append((_field, field))
            else:
                self.stdout.write('There is {} FIELD not in mapping, check mapping var in Command'.format(_field))
                sys.exit(1)
        return ordered_items_mapping

    @staticmethod
    def clean_type(raw_type):
        return raw_type.split('_')[-1]

    def create_bittrex_order(self, row):
        row = dict(row)
        row['account_id'] = 1
        row['exchange_id'] = 1

        order, created = Order.objects.get_or_create(
            uuid=row['uuid'],
            defaults=row
        )
        if created:
            self.total_orders_created += 1

    def get_order_data(self, path):
        ordered_items_mapping = []
        if not path:
            raise CommandError("Please provide file path to CSV file with orders")
        with open(path, 'r') as csvfile:
            spamreader = csv.reader((line.replace('\0', '') for line in csvfile), delimiter=",")
            for counter, row in enumerate(spamreader):
                _result = []
                if not row:
                    continue
                if counter == 0:
                    ordered_items_mapping = self._get_ordered_mapping(row)
                    continue
                for position, item in enumerate(ordered_items_mapping):
                    if item[1] == 'type':
                        clean_value = self.clean_type(row[position])
                    elif item[1] in ['quantity', 'price', 'commission']:
                        clean_value = Decimal(row[position])
                    elif item[1] in ['opened_at', 'closed_at']:
                        clean_value = tz.localize(datetime.strptime(row[position], '%m/%d/%Y %I:%M:%S %p'))
                    elif item[1] == '-':
                        continue
                    else:
                        clean_value = row[position]

                    _result.append((item[1], clean_value))
                yield _result

    def handle(self, *args, **options):
        i = 0
        path = options.get('file')
        iter_order = iter(self.get_order_data(path))
        for order in iter_order:
            i += 1
            self.create_bittrex_order(order)
            if i % 1000 == 0:
                print(i)
        self.stdout.write('Done')
        return
