from django.conf.urls import url

from apps.api.views import (
    APIOrderView, APIStrategyCreateView,
    strategy_set_value_view, strategy_delete_key_view, strategy_delete_view, account_heroku_api_settings_view)

app_name = 'api'

urlpatterns = [
    url(r'^orders/(?P<exchange_name>[\w.@+-]+)/$', APIOrderView.as_view(), name='api_order_list'),
    url(r'^strategy/create/$', APIStrategyCreateView.as_view(), name='api_strategy_create'),
    url(r'^strategy/(?P<strategy_uuid>[\w.@+-]+)/delete/$', strategy_delete_view,
        name='strategy_delete_view'),

    url(r'^strategy/(?P<strategy_uuid>[\w.@+-]+)/key/edit/$', strategy_set_value_view,
        name='strategy_set_value_view'),
    url(r'^strategy/(?P<strategy_uuid>[\w.@+-]+)/key/delete/$', strategy_delete_key_view,
        name='strategy_delete_key_view'),

    url(r'^accounts/$', account_heroku_api_settings_view,
        name='account_heroku_credentials_view'),

]
