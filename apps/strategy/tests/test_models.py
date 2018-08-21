from django.test import TestCase

from apps.strategy.factories import StrategyFactory


class TestStrategyModel(TestCase):
    def setUp(self):
        self.strategy = StrategyFactory()

    def test_setter_saves_value_in_db(self):
        key = "key"
        value = "test value"
        self.strategy.data = {key: value}
        self.strategy.set_value(key, "new value")
        self.strategy.refresh_from_db()
        self.assertEqual(self.strategy.data, {key: "new value"})

    def test_setter_strategy_data(self):
        key = "key"
        value = "test value"
        self.strategy.data = {key: value}
        self.strategy.save(update_fields=['data', ])
        self.assertEqual(self.strategy.data, {key: value})

        self.strategy.set_value(key, "new value")
        self.assertEqual(self.strategy.data[key], "new value")

    def test_delete_key_saves_changes_in_db(self):
        key = "key"
        value = "test value"
        self.strategy.data = {key: value}
        self.strategy.save(update_fields=['data', ])
        self.assertEqual(self.strategy.data, {key: value})

        self.strategy.delete_key(key)
        self.strategy.refresh_from_db()
        self.assertEqual(self.strategy.data, {})
