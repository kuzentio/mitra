from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from apps.strategy.constants import CREATE_STRATEGY_DEFAULTS
from apps.strategy.models import Strategy


class StrategyView(LoginRequiredMixin, generic.ListView):
    model = Strategy
    template_name = 'strategy/strategy_list.html'
    ordering = '-updated_at'

    def get_queryset(self):
        qs = super(StrategyView, self).get_queryset()
        return qs.filter(user=self.request.user, is_deleted=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StrategyView, self).get_context_data()
        context['create_strategy_defaults'] = CREATE_STRATEGY_DEFAULTS
        return context


class StrategyDetailView(generic.DetailView):
    model = Strategy
    template_name = 'strategy/strategy_detail.html'
