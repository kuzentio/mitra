from django.views.generic import TemplateView

from order.forms import OrderPeriodForm


class OrderView(TemplateView):
    template_name = 'order/order_list.html'

    def get_context_data(self,  **kwargs):
        context = super(OrderView, self).get_context_data()
        context['form'] = OrderPeriodForm(self.request.GET)
        context['exchange_name'] = self.kwargs.get('exchange_name', 'none')

        return context
