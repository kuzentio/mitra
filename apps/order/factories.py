import factory

from dateutil.tz import datetime
from factory.fuzzy import FuzzyDecimal, FuzzyChoice

from apps.order import constance
from apps.order.models import Exchange, Order, Price


class ExchangeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Exchange

        django_get_or_create = ('name',)
    name = FuzzyChoice([exchange[0] for exchange in constance.EXCHANGES_CHOICES])
    is_active = True


class OrderFactory(factory.DjangoModelFactory):
    class Meta:
        model = Order
        django_get_or_create = ('uuid', )

    uuid = factory.Faker('uuid4')
    exchange = factory.SubFactory('apps.order.factories.ExchangeFactory')
    account = factory.SubFactory('apps.profile_app.factories.AccountFactory')

    type = factory.Iterator([constance.ORDER_TYPE_BUY, constance.ORDER_TYPE_SELL])
    pair = 'BTC-ETH'

    quantity = FuzzyDecimal(0.01, 1.5)
    commission = FuzzyDecimal(0.0001, 0.101)
    price = FuzzyDecimal(0.025, 2.25)

    opened_at = factory.LazyFunction(datetime.datetime.now)
    closed_at = factory.LazyFunction(datetime.datetime.now)

    data = "{}"


class PriceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Price
        django_get_or_create = ('pair', )
    pair = 'BTC-ETH'
    ask = FuzzyDecimal(0.025, 2.25)
    timestamp = factory.LazyFunction(datetime.datetime.now)
    data = "{}"
