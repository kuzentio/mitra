from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED, HTTP_200_OK

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
