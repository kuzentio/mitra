import decimal
import random

import factory

from dateutil.tz import datetime
from factory.fuzzy import FuzzyDecimal, FuzzyChoice

from order import constance


class ExchangeFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'order.Exchange'
        django_get_or_create = ('name',)
    name = FuzzyChoice([exchange[0] for exchange in constance.EXCHANGES_CHOICES])
    is_active = True


class OrderFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'order.Order'
        django_get_or_create = ('uuid', )

    uuid = factory.Faker('uuid4')
    exchange = factory.SubFactory('order.factories.ExchangeFactory')
    account = factory.SubFactory('profile_app.factories.AccountFactory')

    type = factory.Iterator([constance.ORDER_TYPE_BUY, constance.ORDER_TYPE_SELL])
    pair = 'BTC-ETH'

    quantity = FuzzyDecimal(0.01, 1.5)
    commission = FuzzyDecimal(0.0001, 0.101)
    price = FuzzyDecimal(0.025, 2.25)

    opened_at = factory.LazyFunction(datetime.datetime.now)
    closed_at = factory.LazyFunction(datetime.datetime.now)

    data = "{}"
