from rest_framework import serializers

from apps.order.constants import EXCHANGES_CHOICES
from apps.strategy.constants import CREATE_STRATEGY_DEFAULTS


def validate_secret_length(data):
    keys = data.keys()
    values = data.values()
    for key, value in zip(list(keys), list(values)):
        if key == 'SECRET' and len(value) < 32:
            raise serializers.ValidationError(
                "Enter correct api secret looks like your api secret is less then 32 char"
            )
        if key == 'SECRET' and len(value) > 32:
            raise serializers.ValidationError(
                "Enter correct api secret looks like your api secret is more then 32 char"
            )


def validate_key_length(data):
    keys = data.keys()
    values = data.values()
    for key, value in zip(list(keys), list(values)):
        if key == 'KEY' and len(value) < 32:
            raise serializers.ValidationError(
                "Enter correct api key looks like your api key is less then 32 char"
            )
        if key == 'KEY' and len(value) > 32:
            raise serializers.ValidationError(
                "Enter correct api key looks like your api key is more then 32 char"
            )


def validate_exchange_name(data):
    keys = data.keys()
    values = data.values()
    exchanges = dict(EXCHANGES_CHOICES).keys()
    for key, value in zip(list(keys), list(values)):
        if key == 'EXCHANGE' and value.lower() not in exchanges:
            raise serializers.ValidationError(
                "We do not know about {0} exchange, please choose from - {1}".format(
                    value.lower(), ', '.join(exchanges))
            )


def validate_required_keys(data):
    keys = data.keys()
    for required_key in CREATE_STRATEGY_DEFAULTS.keys():
        if required_key not in keys:
            raise serializers.ValidationError("Missing key - {}".format(required_key))


def validate_white_spaces(data):
    values = data.values()
    for value in values:
        if value.isspace():
            raise serializers.ValidationError("All values should not be empty")


def validate_name_coin(data):
    keys = data.keys()
    values = data.values()
    for key, value in zip(list(keys), list(values)):
        if key == 'NAME_COIN' and value != 'BTC':
            raise serializers.ValidationError(
                "Currently we do not support non BTC trading, please fill NAME_COIN as BTC."
            )
