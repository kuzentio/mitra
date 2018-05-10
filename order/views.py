from django.views.generic import ListView

from order.models import Order


class OrderView(ListView):
    model = Order

    def get_queryset(self):
        qs = super(OrderView, self).get_queryset()
        exchange_name = self.kwargs.get('exchange_name')
        if exchange_name is None:
            return qs
        return qs.filter(exchange__name=exchange_name.lower())
