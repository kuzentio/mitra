from datetime import datetime

from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.api.serializers import OrderSerializer, StrategyCreateSerializer, AccountCreateSerializer
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


class BaseApiCreateView(generics.CreateAPIView):
    serializer_class = StrategyCreateSerializer

    def get_data_from_request(self, request):
        return dict(request.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.get_data_from_request(request))
        if serializer.is_valid():
            serializer.save()

            headers = self.get_success_headers(serializer.data)
            return Response({'success': True}, status=status.HTTP_201_CREATED, headers=headers)

        response_data = serializer.data
        response_data['errors'] = serializer.errors
        response_data['success'] = False
        return Response(response_data, status=status.HTTP_200_OK)


class APIStrategyCreateView(BaseApiCreateView):
    serializer_class = StrategyCreateSerializer

    def get_data_from_request(self, request):
        data = super().get_data_from_request(request)
        data = {
            'data': dict(zip(data['key'], data['value'])),
            'user': request.user.id
        }
        return data


class APIAccountCreateView(BaseApiCreateView):
    serializer_class = AccountCreateSerializer

    def get_data_from_request(self, request):
        data = super().get_data_from_request(request)
        data = {
            'exchange': data.get('exchange')[0],
            'api_key': data.get('api_key')[0],
            'api_secret': data.get('api_secret')[0],
            'user': request.user.id
        }
        return data


@api_view(["POST"])
def strategy_set_value_view(request, strategy_uuid):
    strategy = get_object_or_404(Strategy.objects.filter(uuid=strategy_uuid))
    key = request.POST.get('key', '')
    value = request.POST.get('value', '')
    strategy.set_value(key, value)

    return JsonResponse({'success': True, 'data': strategy.data})


@api_view(["POST"])
def strategy_delete_key_view(request, strategy_uuid):
    strategy = get_object_or_404(Strategy.objects.filter(uuid=strategy_uuid))
    key = request.POST.get('key')
    strategy.delete_key(key)

    return JsonResponse({'success': True, 'data': strategy.data})


@api_view(["POST"])
def strategy_delete_view(request, strategy_uuid):
    strategy = get_object_or_404(Strategy.objects.filter(uuid=strategy_uuid))
    strategy.is_deleted = True
    strategy.save()
    return JsonResponse({'success': True})
