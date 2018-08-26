from django.conf.urls import url

from apps.profile_app import views

app_name = 'profile_app'

urlpatterns = [
    url(
        regex=r'$',
        view=views.AccountsView.as_view(),
        name='accounts'
    ),
]
