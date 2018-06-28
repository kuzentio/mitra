from decimal import Decimal
from django.db.models import Sum, F, Avg

from apps.order.constants import ORDER_TYPE_BUY, ORDER_TYPE_SELL
from apps.order.models import Price


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

    aggregations[ORDER_TYPE_BUY] = round(total_buy, 8)
    aggregations[ORDER_TYPE_SELL] = round(total_sell, 8)
    aggregations['revenue'] = round(total_sell - total_buy, 8)

    return aggregations


def get_avg_price(queryset, type):
    """
    https://www.tradingtechnologies.com/help/fix-adapter-reference/pl-calculation-algorithm/understanding-pl-calculations/
    :param queryset: Order
    :param type: ORDER_TYPE_BUY/ORDER_TYPE_SELL
    :return: tuple(price(Decimal), quantity(Decimal))
    """
    qs = queryset.filter(type=type).all()
    avg_sell_price = qs.annotate(total=(F('quantity') * F('price'))).aggregate(
        Sum('total'),
        Sum('quantity'),
    )
    if avg_sell_price['quantity__sum'] is None:
        return Decimal('0'), Decimal('0')

    price = avg_sell_price['total__sum'] / avg_sell_price['quantity__sum']

    return round(price, 8), avg_sell_price['quantity__sum']


def get_avg_open_price_matched_orders(queryset):
    """
    https://www.tradingtechnologies.com/help/fix-adapter-reference/pl-calculation-algorithm/understanding-pl-calculations/
    :param queryset: Order
    :return: Average buy price for matched orders, it returns 0.0 in case Orders contains many currencies.
    """
    if len(queryset.values_list('pair', flat=True).distinct()) > 1:  # TODO: not implemented
        return Decimal('0.0')
    order_ids = []
    _counter_quantity = Decimal('0.0')
    total_sell_quantity = queryset.all().filter(
        type=ORDER_TYPE_SELL
    ).aggregate(
        quantity=Sum('quantity')
    )['quantity'] or Decimal('0.0')
    for order_id, order_quantity in queryset.select_related().values_list('id', 'quantity').iterator():
        _counter_quantity += order_quantity
        if total_sell_quantity >= _counter_quantity:
            order_ids.append(order_id)
        else:
            break
    avg_price = get_avg_price(queryset.filter(id__in=order_ids), ORDER_TYPE_BUY)

    return avg_price[0]


def get_orders_pnl(queryset):
    """
    https://www.tradingtechnologies.com/help/fix-adapter-reference/pl-calculation-algorithm/understanding-pl-calculations/
    :param queryset: Order
    :return:
    """
    result = {
        'pnl_total': Decimal('0.0'),
        'pnl_realized': Decimal('0.0'),
        'pnl_unrealized': Decimal('0.0'),
        'total_commission': queryset.all().aggregate(Sum('commission'))['commission__sum']
    }
    if len(queryset.values_list('pair', flat=True).distinct()) > 1:
        return result

    buy_price, buy_quantity = get_avg_price(queryset.all(), ORDER_TYPE_BUY)
    sell_price, sell_quantity = get_avg_price(queryset.all(), ORDER_TYPE_SELL)

    result['pnl_realized'] = (sell_price - buy_price) * sell_quantity
    points = buy_quantity - sell_quantity
    avg_open_price = get_avg_open_price_matched_orders(queryset.all())
    if queryset.filter(type=ORDER_TYPE_SELL).exists():
        pair = queryset.values_list('pair', flat=True).distinct()
        try:
            theoretical_sell_price = Price.objects.get(pair=pair[0]).ask
        except (Price.MultipleObjectsReturned, Price.DoesNotExist, AttributeError):
            theoretical_sell_price = Decimal('0.0')
    else:
        theoretical_sell_price = Decimal('0.0')
    result['pnl_unrealized'] = (theoretical_sell_price - avg_open_price) * points
    result['pnl_total'] = result['pnl_realized'] + result['pnl_unrealized']
    result['revenue'] = result['pnl_total'] - result['total_commission']

    return result
