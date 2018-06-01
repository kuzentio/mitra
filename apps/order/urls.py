from django.conf.urls import url

from apps.order import views

app_name = 'order'

urlpatterns = [
    url(
        regex=r'^(?P<exchange_name>[\w.@+-]+)/$',
        view=views.OrderView.as_view(),
        name='list'
    ),
]
