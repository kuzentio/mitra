import csv

import sys

from datetime import datetime
from decimal import Decimal
from django.core.management import BaseCommand, CommandError
from django.utils.timezone import get_current_timezone

from order.models import Order

tz = get_current_timezone()
class Command(BaseCommand):
    help = 'Upload Bittrex orders in CSV format'
    total_orders_created = 0
    field_mapping = (
        ('OrderUuid', 'uuid',),
        ('Exchange', 'pair'),
        ('Type', 'type'),
        ('Quantity', 'quantity'),
        ('Limit', 'price'),
        ('CommissionPaid', 'commission'),
        ('Price', '-'),
        ('Opened', 'opened_at'),
        ('Closed', 'closed_at'),
    )

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def _get_ordered_mapping(self, row):
        ordered_items_mapping = []
        for _field in row:
            field = dict(self.field_mapping).get(_field)
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

    def handle(self, *args, **options):
        path = options.get('file')
        ordered_items_mapping = []
        if not path:
            raise CommandError("Please provide file path to CSV file with orders")
        with open(path, 'r') as csvfile:
            spamreader = csv.reader((line.replace('\0','') for line in csvfile), delimiter=",")
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
                self.create_bittrex_order(_result)
            if self.total_orders_created % 100:
                print('I created over {} Bittrex orders'.format(self.total_orders_created))
        self.stdout.write('Done.')
        return















