from decimal import Decimal
from django.db.models import Sum, F, Avg

from apps.order.constance import ORDER_TYPE_BUY, ORDER_TYPE_SELL


def get_amount_from_avg_order(queryset, _type, _quantity):
    aggregation = queryset.all().filter(
        type=_type
    ).aggregate(
        Avg('price'),
        Sum('commission'),
        Sum('quantity')
    ) or Decimal('0.0')
    _avg_commission_per_unit = Decimal(aggregation['commission__sum']) / Decimal(aggregation['quantity__sum'])

    result = Decimal('0.0')

    if _type == ORDER_TYPE_BUY:
        result = (Decimal(aggregation['price__avg']) + _avg_commission_per_unit) * _quantity
    if _type == ORDER_TYPE_SELL:
        result = (Decimal(aggregation['price__avg']) - _avg_commission_per_unit) * _quantity

    return result


def get_not_matched_quantity(queryset):
    sell = queryset.filter(
        type=ORDER_TYPE_SELL
    ).aggregate(
        Sum('quantity')
    )
    buy = queryset.filter(
        type=ORDER_TYPE_BUY
    ).aggregate(
        Sum('quantity')
    )
    buy['quantity__sum'] = buy['quantity__sum'] or Decimal('0.0')
    sell['quantity__sum'] = sell['quantity__sum'] or Decimal('0.0')
    _type = ORDER_TYPE_BUY if buy['quantity__sum'] >= sell['quantity__sum'] else ORDER_TYPE_SELL

    return _type, buy['quantity__sum'] - sell['quantity__sum']


def aggregate_orders_by_types(queryset):
    aggregations = dict()
    aggregations['pairs'] = list(
        queryset.values_list('pair', flat=True).distinct()
    )

    total_buy = aggregations[ORDER_TYPE_BUY] = Decimal('0.0')
    total_sell = aggregations[ORDER_TYPE_SELL] = Decimal('0.0')

    if aggregations['pairs']:
        for any_type in [ORDER_TYPE_SELL, ORDER_TYPE_BUY]:
            aggregations[any_type] = queryset.filter(
                type=any_type
            ).annotate(
                total=(F('quantity') * F('price')),
            ).aggregate(
                Sum('total'),
                Sum('commission')
            )
        _type, _quantity = get_not_matched_quantity(queryset.all())
        if _quantity:
            avg_amount = get_amount_from_avg_order(
                queryset, _type, _quantity
            )
            aggregations[_type]['total__sum'] = aggregations[_type]['total__sum'] - avg_amount

        total_buy = aggregations[ORDER_TYPE_BUY].pop('total__sum') + aggregations[ORDER_TYPE_BUY].pop('commission__sum')
        total_sell = aggregations[ORDER_TYPE_SELL].pop('total__sum') - aggregations[ORDER_TYPE_SELL].pop('commission__sum')

    aggregations[ORDER_TYPE_BUY] = total_buy
    aggregations[ORDER_TYPE_SELL] = total_sell
    aggregations['revenue'] = total_sell - total_buy

    return aggregations
