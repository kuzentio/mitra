from django.conf.urls import url

from order import views

urlpatterns = [
    url(
        regex=r'^(?P<exchange_name>[\w.@+-]+)/$',
        view=views.OrderView.as_view(),
        name='list'
    ),
]
