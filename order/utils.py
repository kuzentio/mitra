from django.db.models import Avg

from order import constance


def aggregate_orders_by_types(queryset):
    aggregations = {}

    for any_type in [constance.ORDER_TYPE_SELL, constance.ORDER_TYPE_BUY]:
        if queryset.filter(type=any_type).exists():
            aggregations[any_type] = queryset.filter(
                type=any_type
            ).aggregate(
                Avg('price'),
                Avg('quantity'),
                Avg('commission')
            )
            price = aggregations[any_type]['price__avg']
            quantity = aggregations[any_type]['quantity__avg']
            commission = aggregations[any_type]['commission__avg']
            avg_pull_per_order = (price * quantity) - commission
            aggregations[any_type]['avg_pull_per_order'] = avg_pull_per_order

    return aggregations
