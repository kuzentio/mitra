from rest_framework import serializers

from apps.order.models import Order
from apps.strategy import validators
from apps.strategy.models import Strategy


class OrderSerializer(serializers.ModelSerializer):
    closed_at = serializers.DateTimeField(format='%d.%m.%Y %I:%M:%S %p')
    exchange = serializers.SerializerMethodField()

    @staticmethod
    def get_exchange(obj):
        return obj.exchange.name

    class Meta:
        model = Order
        fields = '__all__'


class StrategyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Strategy
        fields = ('data', 'user')
        extra_kwargs = {
            "data": {
                "validators": [
                    validators.validate_required_keys,
                    validators.validate_white_spaces,

                    validators.validate_key_length,
                    validators.validate_secret_length,
                    validators.validate_exchange_name,
                    validators.validate_name_coin,
                ]
            }
        }
