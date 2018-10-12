from django import forms

from apps.profile_app.models import HerokuCredentials


class HerokuCredentialsForm(forms.ModelForm):
    class Meta:
        model = HerokuCredentials
        fields = ['api_key', ]
