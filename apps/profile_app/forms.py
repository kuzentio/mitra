from django import forms
from django.forms import widgets

from apps.profile_app.models import Account


class AccountCreateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('exchange', 'api_key', 'api_secret')

        base_widget = widgets.Input(attrs={'class': 'form-control'})
        widgets = {
            'exchange': base_widget,
            'api_key': base_widget,
            'api_secret': base_widget,

        }
