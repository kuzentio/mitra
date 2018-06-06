from datetime import datetime

from rest_framework import generics

from apps.api.serializers import OrderSerializer
from apps.order import utils
from apps.order import constance
from apps.order.models import Order


class APIOrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        extra_query = {}
        qs = super(APIOrderView, self).get_queryset()
        closed_at_range = [
            constance.DEFAULT_MIN_DATE,
            constance.DEFAULT_MAX_DATE,
        ]

        if self.request.query_params.get('min_date'):
            min_date = datetime.strptime(
                self.request.query_params.get('min_date'), '%d.%m.%Y'
            )
            closed_at_range[0] = min_date

        if self.request.query_params.get('max_date'):
            max_date = datetime.strptime(
                self.request.query_params.get('max_date'), '%d.%m.%Y'
            )
            closed_at_range[1] = max_date
        extra_query['closed_at__range'] = closed_at_range

        extra_query['pair__icontains'] = self.request.query_params.get('pair', '')

        exchange = self.kwargs.get('exchange_name')
        if exchange is not None:
            extra_query['exchange__name'] = exchange

        return qs.filter(**extra_query)

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(APIOrderView, self).finalize_response(request, response)

        pnl = utils.get_orders_pnl(self.get_queryset().all())
        response.data.update(pnl)
        response.data.update(
            {'pairs': list(self.get_queryset().all().values_list('pair', flat=True).distinct())}
        )
        return response
