from decimal import Decimal
from django.db.models import Sum, F, Avg

from order import constance


def get_amount_from_avg_order(queryset, _type, _quantity):
    aggregation = queryset.all().filter(
        type=_type
    ).aggregate(
        Avg('price'),
    ) or Decimal('0.0')
    result = Decimal(aggregation['price__avg']) * _quantity

    return result


def get_not_matched_quantity(queryset):
    sell = queryset.filter(
        type=constance.ORDER_TYPE_SELL
    ).aggregate(
        Sum('quantity')
    )
    buy = queryset.filter(
        type=constance.ORDER_TYPE_BUY
    ).aggregate(
        Sum('quantity')
    )
    buy['quantity__sum'] = buy['quantity__sum'] or Decimal('0.0')
    sell['quantity__sum'] = sell['quantity__sum'] or Decimal('0.0')
    _type = constance.ORDER_TYPE_BUY if buy['quantity__sum'] >= sell['quantity__sum'] else constance.ORDER_TYPE_SELL

    return _type, buy['quantity__sum'] - sell['quantity__sum']


def aggregate_orders_by_types(queryset):
    aggregations = {}

    for any_type in [constance.ORDER_TYPE_SELL, constance.ORDER_TYPE_BUY]:
        aggregations[any_type] = queryset.filter(
            type=any_type
        ).annotate(
            total=(F('quantity') * F('price')),
        ).aggregate(
            Sum('total'),
        )
    _type, _quantity = get_not_matched_quantity(queryset.all())
    if _quantity:
        aggregations[_type]['total__sum'] = aggregations[_type]['total__sum'] - get_amount_from_avg_order(queryset, _type, _quantity)

    total_buy = aggregations[constance.ORDER_TYPE_BUY].pop('total__sum') or Decimal('0.0')
    total_sell = aggregations[constance.ORDER_TYPE_SELL].pop('total__sum') or Decimal('0.0')

    aggregations[constance.ORDER_TYPE_BUY] = total_buy
    aggregations[constance.ORDER_TYPE_SELL] = total_sell
    aggregations['revenue'] = total_sell - total_buy

    return aggregations
