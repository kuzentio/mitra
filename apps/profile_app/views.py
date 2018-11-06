from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AccountsView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_app/accounts.html'
