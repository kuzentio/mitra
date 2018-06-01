from django.conf.urls import url

from apps.api.views import APIOrderView

app_name = 'api'

urlpatterns = [
    url(r'^orders/(?P<exchange_name>[\w.@+-]+)/$', APIOrderView.as_view(), name='api_order_list')
]
