from django.views.generic import ListView

from order.models import Order


class OrderView(ListView):
    model = Order
    paginate_by = 50

    def get_queryset(self):
        qs = super(OrderView, self).get_queryset()
        exchange_name = self.kwargs.get('exchange_name')
        if not exchange_name:
            return qs
        return qs.filter(exchange__name=exchange_name.lower())
