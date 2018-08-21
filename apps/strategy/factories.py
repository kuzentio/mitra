import datetime
import factory

from apps.profile_app.factories import UserFactory
from apps.strategy.models import Strategy


class StrategyFactory(factory.DjangoModelFactory):
    class Meta:
        model = Strategy
        django_get_or_create = ('uuid', )

    uuid = factory.Faker('uuid4')
    user = factory.SubFactory(UserFactory)

    data = dict()
    is_deleted = False
    updated_at = factory.LazyFunction(datetime.datetime.now)
    created_at = factory.LazyFunction(datetime.datetime.now)
