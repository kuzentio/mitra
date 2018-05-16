from django.db.models import Avg
from rest_framework import generics

from api.serializers import OrderSerializer
from order import utils
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

    def get_aggregations(self):
        qs = self.filter_queryset(
            self.get_queryset()
        )
        aggregations = utils.aggregate_orders_by_types(qs)

        return aggregations

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(APIOrderView, self).finalize_response(request, response)
        response.data.update(self.get_aggregations())
        return response
