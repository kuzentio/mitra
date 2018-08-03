from django.conf.urls import url

from apps.strategy.views import StrategyView, StrategyDetailView

app_name = 'strategy'

urlpatterns = [
    url(regex=r'^$', view=StrategyView.as_view(), name='list'),
    url(regex=r'^(?P<strategy__uuid>[\d\w-]+)/$', view=StrategyDetailView.as_view(), name='detail'),
]
