from django.test import TestCase, Client
from django.urls import reverse

from apps.profile_app.factories import AccountFactory, UserFactory
from apps.profile_app.models import Account

client = Client()


class TestStrategyListView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.set_password('123')
        self.user.save()
        self.account = AccountFactory(user=self.user)

    def test_account_list_view_success(self):
        client.login(username=self.user.username, password='123')

        response = client.get(reverse('profile_app:accounts'))
        self.assertEqual(
            list(response.context[0]['account_list']), list(Account.objects.filter(user=self.user, is_active=True))
        )
