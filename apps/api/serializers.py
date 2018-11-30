from rest_framework import serializers

from apps.order.models import Order, Exchange
from apps.profile_app.models import Account
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
        fields = ('data', 'user', 'port')
        extra_kwargs = {
            "data": {
                "validators": [
                    validators.validate_required_keys,
                    validators.validate_white_spaces,

                    validators.validate_exchange_name,
                    validators.validate_name_coin,
                ]
            }
        }


class AccountCreateSerializer(serializers.ModelSerializer):
    exchange = serializers.CharField()
    api_key = serializers.CharField()
    api_secret = serializers.CharField()

    class Meta:
        model = Account
        fields = ('user', 'exchange', 'api_key', 'api_secret')

    def validate_exchange(self, exchange_name):
        validators.validate_exchange_name({'EXCHANGE': exchange_name})
        try:
            exchange = Exchange.objects.get(name=exchange_name)
        except Exchange.DoesNotExist:
            raise serializers.ValidationError("Could not find any exchanges for this name.")

        return exchange
