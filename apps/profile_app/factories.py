import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from apps.order.factories import ExchangeFactory
from apps.profile_app.models import Account


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )
    first_name = "Ihor"
    last_name = "Kuzmenko"
    username = "hello@test.com"
    password = make_password('password')


class AccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = Account
        django_get_or_create = ('user', )

    user = factory.SubFactory(UserFactory)
    # exchange = factory.SubFactory('apps.order.factories.ExchangeFactory')
    exchange = factory.SubFactory(ExchangeFactory)
    email = 'email@example.com'
    username = factory.Faker('user_name')
    password = factory.Faker('name')
    api_key = 'AWESOMEAPIKEY'
    api_secret = 'AWESOMEAPISECRET'
