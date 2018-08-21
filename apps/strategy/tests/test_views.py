from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from apps.strategy.factories import StrategyFactory
from apps.strategy.models import Strategy

client = Client()


class TestStrategyListView(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', username='test')
        self.user.set_password('123')
        self.user.save()
        self.strategy = StrategyFactory(user=self.user)

    def test_strategy_list_view(self):
        client.login(username=self.user.username, password='123')

        response = client.get(reverse('strategy:list'))
        self.assertEqual(
            list(response.context[0]['strategy_list']), list(Strategy.objects.filter(user=self.user, is_deleted=False))
        )
