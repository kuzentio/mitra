from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.order import views

app_name = 'order'

urlpatterns = [
    url(
        regex=r'^(?P<exchange_name>[\w.@+-]+)/$',
        view=login_required(views.OrderView.as_view()),
        name='list'
    ),
]
