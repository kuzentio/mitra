from datetime import datetime

from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response

from apps.api.serializers import OrderSerializer, StrategyCreateSerializer
from apps.order import utils
from apps.order import constants
from apps.order.models import Order
from apps.strategy.models import Strategy


class APIOrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        extra_query = {}
        qs = super(APIOrderView, self).get_queryset()
        closed_at_range = [
            constants.DEFAULT_MIN_DATE,
            constants.DEFAULT_MAX_DATE,
        ]

        if self.request.query_params.get('pair') == 'All':
            self.request.GET._mutable = True
            self.request.query_params.pop('pair')

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
        if self.get_queryset().exists():
            pnl = utils.get_orders_pnl(self.get_queryset().all())
            response.data.update(pnl)
        response.data.update(
            {'pairs': list(self.get_queryset().all().values_list('pair', flat=True).distinct())}
        )
        return response


class APIStrategyCreateView(generics.CreateAPIView):
    serializer_class = StrategyCreateSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        strategy_data = dict(
            zip(data['key'], data['value'])
        )
        serializer = self.serializer_class(data={
            'data': strategy_data,
            'user': request.user.id
        })
        if serializer.is_valid():
            serializer.save()

            headers = self.get_success_headers(serializer.data)
            return Response({'success': True}, status=status.HTTP_201_CREATED, headers=headers)

        response_data = serializer.data
        response_data['errors'] = serializer.errors
        response_data['success'] = False
        return Response(data=response_data, status=status.HTTP_200_OK, )


def api_strategy_edit_view(request, strategy_uuid):
    strategy = get_object_or_404(Strategy.objects.filter(uuid=strategy_uuid))
    key = request.POST.get('key')
    value = request.POST.get('value')
    strategy.set_value(key, value)

    return JsonResponse({'success': True, 'data': strategy.data})
