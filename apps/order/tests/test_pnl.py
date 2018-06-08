from decimal import Decimal
from django.test import TestCase

from apps.order.constance import ORDER_TYPE_BUY, ORDER_TYPE_SELL
from apps.order.factories import OrderFactory
from apps.order.models import Order
from apps.order.utils import (
    get_avg_price, get_avg_open_price_matched_orders
)
from apps.profile_app.factories import AccountFactory


class TestPNLUtils(TestCase):
    def setUp(self):
        self.account = AccountFactory()
        self.order_quantity = Decimal('1.0')
        self.order_commission = Decimal('0.5')
        self.order_price = Decimal('10.0')

    def test_get_avg_price_by_buy(self):
        for i in range(0, 4):
            OrderFactory.create(
                type=ORDER_TYPE_BUY,
                account=self.account,
                pair='BTC-MANA',
                quantity=self.order_quantity,
                commission=self.order_commission,
                price=self.order_price,
            )
        avg_price_buy = get_avg_price(Order.objects.all(), type=ORDER_TYPE_BUY)
        avg_price_sell = get_avg_price(Order.objects.all(), type=ORDER_TYPE_SELL)

        self.assertEqual(avg_price_buy, (self.order_price, self.order_quantity * 4))
        self.assertEqual(avg_price_sell, (Decimal('0'), Decimal('0')))

    def test_get_avg_price_without_orders(self):
        avg_price_buy = get_avg_price(Order.objects.all(), type=ORDER_TYPE_BUY)
        avg_price_sell = get_avg_price(Order.objects.all(), type=ORDER_TYPE_SELL)

        self.assertEqual(avg_price_buy, (Decimal('0'), Decimal('0')))
        self.assertEqual(avg_price_sell, (Decimal('0'), Decimal('0')))

    def test_get_avg_price_with_different_price(self):
        OrderFactory.create(
            type=ORDER_TYPE_BUY,
            account=self.account,
            pair='BTC-MANA',
            quantity=self.order_quantity,
            commission=self.order_commission,
            price=Decimal('10.0'),
        )
        OrderFactory.create(
            type=ORDER_TYPE_BUY,
            account=self.account,
            pair='BTC-MANA',
            quantity=self.order_quantity,
            commission=self.order_commission,
            price=Decimal('30.0'),
        )
        avg_price_buy = get_avg_price(Order.objects.all(), type=ORDER_TYPE_BUY)
        self.assertEqual(avg_price_buy, (Decimal('20.0'), self.order_quantity * 2))

    def test_get_avg_open_price_matched_orders(self):
        BUY_PRICE = Decimal('9.0')
        for i in range(0, 4):
            OrderFactory.create(
                type=ORDER_TYPE_BUY,
                account=self.account,
                pair='BTC-MANA',
                quantity=Decimal('10.0'),
                commission=self.order_commission,
                price=BUY_PRICE,
            )
        for i in range(0, 2):
            OrderFactory.create(
                type=ORDER_TYPE_SELL,
                account=self.account,
                pair='BTC-MANA',
                quantity=Decimal('15.0'),
                commission=self.order_commission,
                price=Decimal('15.0'),
            )
        avg_price = get_avg_open_price_matched_orders(Order.objects.all())
        self.assertEqual(avg_price, BUY_PRICE)

    def test_get_average_price_with_different_buy_prices(self):
        PRICE_1 = Decimal('10.0')
        PRICE_2 = Decimal('12.0')
        OrderFactory.create(
            type=ORDER_TYPE_BUY,
            account=self.account,
            pair='BTC-MANA',
            quantity=Decimal('10.0'),
            commission=self.order_commission,
            price=PRICE_1,
        )
        OrderFactory.create(
            type=ORDER_TYPE_BUY,
            account=self.account,
            pair='BTC-MANA',
            quantity=Decimal('10.0'),
            commission=self.order_commission,
            price=PRICE_2,
        )
        OrderFactory.create(
            type=ORDER_TYPE_SELL,
            account=self.account,
            pair='BTC-MANA',
            quantity=Decimal('20.0'),
            commission=self.order_commission,
            price=PRICE_2 + Decimal('1.0'),
        )
        avg_price = get_avg_open_price_matched_orders(Order.objects.all())
        self.assertEqual(avg_price, Decimal('11.00'))

    def test_get_average_price_returns_zero_if_orders_are_not_matched(self):
        for i in range(0, 5):
            OrderFactory.create(
                type=ORDER_TYPE_BUY,
                account=self.account,
                pair='BTC-MANA',
                quantity=Decimal('20.0'),
                commission=self.order_commission,
                price=Decimal('15.0'),
            )
        avg_price = get_avg_open_price_matched_orders(Order.objects.all())
        self.assertEqual(avg_price, Decimal('0.0'))

        Order.objects.all().update(type=ORDER_TYPE_SELL)
        avg_price = get_avg_open_price_matched_orders(Order.objects.all())
        self.assertEqual(avg_price, Decimal('0.0'))

    def test_get_average_price_returns_zero_if_passes_many_pairs(self):
        for i in range(0, 6):
            OrderFactory.create(
                account=self.account,
                pair='BTC-MANA',
            )
        for i in range(0, 6):
            OrderFactory.create(
                account=self.account,
                pair='BTC-ETH',
            )
        avg_price = get_avg_open_price_matched_orders(Order.objects.all())
        self.assertEqual(avg_price, Decimal('0.0'))
