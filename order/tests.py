import decimal
import random

from django.db.models import Avg
from django.test import TestCase

from order.factories import OrderFactory
from order.models import Order
from order.utils import aggregate_orders_by_types
from profile.factories import AccountFactory


class TestOrderCreation(TestCase):
    def test_aggregation_orders_by_types_success(self):
        account = AccountFactory()
        for i in range(1, 20):
            OrderFactory(
                account=account,
                pair='BTC-MANA',
                quantity=decimal.Decimal(random.randrange(10, 35))/100,
                commission=decimal.Decimal(random.randrange(1, 5))/1000,
                price=decimal.Decimal(random.randrange(10, 50))/1000,
            )
        payload = aggregate_orders_by_types(Order.objects.all())

        expected_data = {
            "BUY": Order.objects.filter(type='BUY').aggregate(
                Avg('price'),
                Avg('quantity'),
                Avg('commission')
            ),
            "SELL": Order.objects.filter(type='SELL').aggregate(
                Avg('price'),
                Avg('quantity'),
                Avg('commission')
            )
        }




