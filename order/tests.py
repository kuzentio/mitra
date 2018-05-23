from decimal import Decimal
from django.test import TestCase

from order.constance import ORDER_TYPE_BUY, ORDER_TYPE_SELL
from order.factories import OrderFactory
from order.models import Order
from order.utils import aggregate_orders_by_types, get_amount_from_avg_order
from profile.factories import AccountFactory


class TestOrderCreation(TestCase):
    def setUp(self):
        self.account = AccountFactory()
        self.order_quantity = Decimal('1.0')
        self.order_commission = Decimal('0.5')
        self.order_price = Decimal('10.0')

    def test_utils_aggregation_orders_by_types(self):
        for i in range(0, 6):
            OrderFactory.create(
                account=self.account,
                pair='BTC-MANA',
                quantity=self.order_quantity,
                commission=self.order_commission,
                price=self.order_price,
            )
        payload = aggregate_orders_by_types(Order.objects.all())
        payload.pop('revenue')
        self.assertDictEqual(
            {
                'pairs': ['BTC-MANA'],
                'BUY': ((self.order_quantity * self.order_price) + self.order_commission) * 3,
                'SELL': ((self.order_quantity* self.order_price) - self.order_commission) * 3,
            }, payload
        )

    def test_utils_aggregation_orders_with_not_matched_orders(self):
        for i in range(0, 7):
            OrderFactory.create(
                account=self.account,
                pair='BTC-MANA',
                quantity=self.order_quantity,
                commission=self.order_commission,
                price=self.order_price,
            )
        payload = aggregate_orders_by_types(Order.objects.all())
        payload.pop('revenue')

        self.assertDictEqual(
            {
                'pairs': ['BTC-MANA'],
                'BUY': ((self.order_quantity * self.order_price) + self.order_commission) * 3,
                'SELL': ((self.order_quantity * self.order_price) - self.order_commission) * 3,
            }, payload
        )

    def test_utils_get_amount_from_avg_order_for_type_sell(self):
        for i in range(0, 7):
            OrderFactory.create(
                account=self.account,
                pair='BTC-MANA',
                quantity=self.order_quantity,
                commission=self.order_commission,
                price=self.order_price,
            )

        amount = get_amount_from_avg_order(Order.objects.all(), ORDER_TYPE_SELL, self.order_quantity)
        self.assertEqual(amount, (self.order_price * self.order_quantity) - self.order_commission)

    def test_utils_get_amount_from_avg_order_for_type_buy(self):
        for i in range(0, 2):
            OrderFactory.create(
                account=self.account,
                pair='BTC-MANA',
                type=ORDER_TYPE_SELL,
                quantity=self.order_quantity,
                commission=self.order_commission,
                price=self.order_price,
            )
        for i in range(0, 4):
            OrderFactory.create(
                account=self.account,
                pair='BTC-MANA',
                type=ORDER_TYPE_BUY,
                quantity=self.order_quantity,
                commission=self.order_commission,
                price=self.order_price,
            )
        amount = get_amount_from_avg_order(Order.objects.all(), ORDER_TYPE_SELL, self.order_quantity)
        self.assertEqual(amount, (self.order_price * self.order_quantity) - self.order_commission)
