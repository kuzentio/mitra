from django.conf.urls import url

from apps.api.views import (
    APIOrderView, APIStrategyCreateView,
    strategy_set_value_view, strategy_delete_key_view, strategy_delete_view, APIAccountCreateView,
    start_strategy_view, down_strategy_view,
    close_orders_view)

app_name = 'api'

urlpatterns = [
    url(r'^orders/(?P<exchange_name>[\w.@+-]+)/$', APIOrderView.as_view(), name='api_order_list'),
    url(r'^strategy/create/$', APIStrategyCreateView.as_view(), name='api_strategy_create'),
    url(r'^account/create/$', APIAccountCreateView.as_view(), name='api_account_create'),

    url(r'^strategy/(?P<strategy_uuid>[\w.@+-]+)/manage/up/$', start_strategy_view,
        name='start_strategy_view'),
    url(r'^strategy/(?P<strategy_uuid>[\w.@+-]+)/manage/down/$', down_strategy_view,
        name='down_strategy_view'),

    url(r'^strategy/(?P<strategy_uuid>[\w.@+-]+)/manage/close_orders/$', close_orders_view,
        name='close_orders_view'),


    url(r'^strategy/(?P<strategy_uuid>[\w.@+-]+)/delete/$', strategy_delete_view,
        name='strategy_delete_view'),

    url(r'^strategy/(?P<strategy_uuid>[\w.@+-]+)/key/edit/$', strategy_set_value_view,
        name='strategy_set_value_view'),
    url(r'^strategy/(?P<strategy_uuid>[\w.@+-]+)/key/delete/$', strategy_delete_key_view,
        name='strategy_delete_key_view')
]
