from django.conf.urls import url

from apps.api.views import (
    APIOrderView, APIStrategyCreateView,
    api_strategy_edit_view)

app_name = 'api'

urlpatterns = [
    url(r'^orders/(?P<exchange_name>[\w.@+-]+)/$', APIOrderView.as_view(), name='api_order_list'),
    url(r'^strategy/create/$', APIStrategyCreateView.as_view(), name='api_strategy_create'),
    url(r'^strategy/(?P<strategy_uuid>[\w.@+-]+)/edit/$', api_strategy_edit_view,
        name='api_strategy_variable_edit')
]
