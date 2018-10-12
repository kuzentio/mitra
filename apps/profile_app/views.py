from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.profile_app.forms import HerokuCredentialsForm
from apps.profile_app.models import HerokuCredentials


class AccountsView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_app/accounts.html'

    def get_context_data(self, **kwargs):
        context = super(AccountsView, self).get_context_data(**kwargs)

        user = self.request.user
        heroku, _ = HerokuCredentials.objects.get_or_create(user=user)
        context['heroku'] = heroku
        context['heroku_form'] = HerokuCredentialsForm(instance=heroku)

        return context
