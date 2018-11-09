from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from apps.profile_app.constants import CREATE_ACCOUNT_DEFAULTS
from apps.profile_app.forms import AccountCreateForm
from apps.profile_app.models import Account


class AccountsView(LoginRequiredMixin, generic.ListView):
    template_name = 'profile_app/account_list.html'
    model = Account

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['create_account_defaults'] = CREATE_ACCOUNT_DEFAULTS
        context['create_account_form'] = AccountCreateForm
        return context
