from rest_framework import serializers

from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    closed_at = serializers.DateTimeField(format='%d.%m.%Y %I:%M:%S %p')
    exchange = serializers.SerializerMethodField()

    def get_exchange(self, obj):
        return obj.exchange.name

    class Meta:
        model = Order
        fields = '__all__'
