from decimal import Decimal
from django.test import TestCase

from apps.order.constance import ORDER_TYPE_BUY, ORDER_TYPE_SELL
from apps.order.factories import OrderFactory
from apps.order.models import Order
from apps.order.utils import aggregate_orders_by_types, get_amount_from_avg_order, get_not_matched_quantity
from apps.profile_app.factories import AccountFactory


class TestOrderUtils(TestCase):
    def setUp(self):
        self.account = AccountFactory()
        self.order_quantity = Decimal('1.0')
        self.order_commission = Decimal('0.5')
        self.order_price = Decimal('10.0')

    def test_aggregation_orders_by_types(self):
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

    def test_aggregation_orders_with_not_matched_orders(self):
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

    def test_get_amount_from_avg_order_for_type_sell(self):
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

    def test_get_amount_from_avg_order_for_type_buy(self):
        for i in range(0, 2):
            OrderFactory.create(
                type=ORDER_TYPE_SELL,

                account=self.account,
                pair='BTC-MANA',
                quantity=self.order_quantity,
                commission=self.order_commission,
                price=self.order_price,
            )
        for i in range(0, 4):
            OrderFactory.create(
                type=ORDER_TYPE_BUY,

                account=self.account,
                pair='BTC-MANA',
                quantity=self.order_quantity,
                commission=self.order_commission,
                price=self.order_price,
            )
        amount = get_amount_from_avg_order(Order.objects.all(), ORDER_TYPE_SELL, self.order_quantity)
        self.assertEqual(amount, (self.order_price * self.order_quantity) - self.order_commission)

    def test_get_not_matched_quantity(self):
        for i in range(0, 4):
            OrderFactory.create(
                type=ORDER_TYPE_BUY,

                account=self.account,
                pair='BTC-MANA',
                quantity=self.order_quantity,
                commission=self.order_commission,
                price=self.order_price,
            )
        for i in range(0, 1):
            OrderFactory.create(
                type=ORDER_TYPE_SELL,

                account=self.account,
                pair='BTC-MANA',
                quantity=self.order_quantity,
                commission=self.order_commission,
                price=self.order_price,
            )

        payload = get_not_matched_quantity(Order.objects.all())
        expected_not_matched_amount = Decimal(self.order_quantity * 3)

        self.assertIsInstance(payload, tuple)
        self.assertEqual(len(payload), 2)
        self.assertEqual(payload, (ORDER_TYPE_BUY, expected_not_matched_amount))
