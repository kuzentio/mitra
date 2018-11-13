from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED, HTTP_200_OK, HTTP_201_CREATED

from apps.order.constants import EXCHANGES_CHOICES
from apps.profile_app.factories import UserFactory
from apps.strategy.factories import StrategyFactory

client = Client()


class TestStrategyDeleteView(TestCase):
    def setUp(self):
        self.strategy = StrategyFactory()

    def test_strategy_delete_view_do_not_process_get(self):
        response = client.get(
            reverse('api:strategy_delete_view', args=(self.strategy.uuid, ))
        )
        self.assertTrue(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_strategy_set_value_view(self):
        key = "key"
        value = "value"
        new_value = "new value"
        self.strategy.data = {key: value}
        self.strategy.save(update_fields=['data', ])

        response = client.post(
            reverse('api:strategy_set_value_view', args=(self.strategy.uuid, )), data={"key": key, "value": new_value}
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['data']['key'], new_value)

    def test_strategy_delete_key_view(self):
        key = "key"
        value = "value"
        self.strategy.data = {key: value}
        self.strategy.save(update_fields=['data', ])

        response = client.post(
            reverse('api:strategy_delete_key_view', args=(self.strategy.uuid,)), data={"key": key}
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()['data'], dict())

    def test_strategy_delete_key_view_does_not_affect_another_keys(self):
        key = "key"
        value = "value"
        test_data = {
            key: value,
            "test-key-1": "Test value 1",
            "test-key-2": "Test value 2",
        }
        self.strategy.data = test_data
        self.strategy.save(update_fields=['data', ])

        response = client.post(
            reverse('api:strategy_delete_key_view', args=(self.strategy.uuid,)), data={"key": key}
        )

        del test_data[key]
        self.assertEqual(response.json()['data'], test_data)


class TestAccountCreateView(TestCase):
    def test_creating_account_success(self):
        api_key, api_secret = "K" * 32, "S" * 32
        test_account = {
            "exchange": EXCHANGES_CHOICES[0][0],
            "api_key": api_key,
            "api_secret": api_secret,
        }
        admin = UserFactory(username='admin')
        client.force_login(admin)

        response = client.post(reverse("api:api_account_create"), data=test_account)
        data = response.json()
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(data['data']['user'], admin.id)
        self.assertEqual(data['data']['api_key'], api_key)
        self.assertEqual(data['data']['api_secret'], api_secret)

    def test_creating_account_without_exchange(self):
        api_key, api_secret = "K" * 32, "S" * 32
        teset_account = {
            "api_key": api_key,
            "api_secret": api_secret,
        }
        response = client.post(reverse("api:api_account_create"), data=teset_account)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['errors']['exchange'], ['This field may not be null.', ])

    def test_creating_account_without_api_credentials_raises_exception(self):
        test_account = {
            "exchange": EXCHANGES_CHOICES[0][0],
        }
        response = client.post(reverse("api:api_account_create"), data=test_account)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['errors']['api_key'], ['This field may not be null.', ])
        self.assertEqual(data['errors']['api_secret'], ['This field may not be null.', ])


class TestStrategyCreateView(TestCase):
    def test_creating_strategy_success(self):
        test_strategy = {
            "key": ["EXCHANGE", "KEY", "SECRET", "NAME_COIN", "NAME_COIN_TWO"],
            "value": ["bittrex", "K" * 32, "S" * 32, "BTC", "ETH"],
        }
        admin = UserFactory(username='admin')
        client.force_login(admin)

        response = client.post(reverse("api:api_strategy_create"), data=test_strategy)
        data = response.json()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['data']['user'], admin.id)

    def test_creating_account_without_exchange(self):
        api_key, api_secret = "K" * 32, "S" * 32
        teset_account = {
            "api_key": api_key,
            "api_secret": api_secret,
        }
        response = client.post(reverse("api:api_account_create"), data=teset_account)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['errors']['exchange'], ['This field may not be null.', ])

    def test_creating_account_without_api_credentials_raises_exception(self):
        test_account = {
            "exchange": EXCHANGES_CHOICES[0][0],
        }
        response = client.post(reverse("api:api_account_create"), data=test_account)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['errors']['api_key'], ['This field may not be null.', ])
        self.assertEqual(data['errors']['api_secret'], ['This field may not be null.', ])
