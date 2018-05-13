from django.views.generic import ListView

from order.models import Order


class OrderView(ListView):
    model = Order

    def get_context_data(self,  **kwargs):
        context = super(OrderView, self).get_context_data()
        context['exchange_name'] = self.kwargs.get('exchange_name', 'none')

        return context
