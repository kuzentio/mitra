from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.order.forms import OrderPeriodForm
from apps.order.models import Exchange


class OrderView(LoginRequiredMixin, TemplateView):
    template_name = 'order/order_list.html'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Exchange, name=self.kwargs['exchange_name'])
        return super(OrderView, self).dispatch(request)

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data()
        context['form'] = OrderPeriodForm(self.request.GET)
        context['exchange_name'] = self.kwargs.get('exchange_name', 'none')

        return context
