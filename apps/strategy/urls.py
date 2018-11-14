from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.strategy.views import StrategyView, StrategyDetailView

app_name = 'strategy'

urlpatterns = [
    url(regex=r'^$', view=login_required(StrategyView.as_view()), name='list'),
    url(regex=r'^(?P<strategy__uuid>[\d\w-]+)/$', view=login_required(StrategyDetailView.as_view()), name='detail'),
]
