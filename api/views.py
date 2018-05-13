from rest_framework import generics

from api.serializers import OrderSerializer
from order.models import Order


class APIOrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super(APIOrderView, self).get_queryset()
        exchange = self.kwargs.get('exchange_name')
        if exchange is not None:
            return qs.filter(exchange__name=exchange)
        return qs
