from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.profile_app import views

app_name = 'profile_app'

urlpatterns = [
    url(
        regex=r'$',
        view=login_required(views.AccountsView.as_view()),
        name='accounts'
    ),
]
