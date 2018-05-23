from django import forms
from django.forms import widgets


class OrderPeriodForm(forms.Form):
    min_date = forms.DateField(
        input_formats='%m/%d/%Y',
        required=False,
        label='From:',
        widget=widgets.Input(
            attrs={'class': 'form-control date_range_filter date'}
        )
    )
    max_date = forms.DateField(
        input_formats='%m/%d/%Y',
        required=False,
        label='To:',
        widget=widgets.Input(
            attrs={'class': 'form-control date_range_filter date'}
        )
    )
    pair = forms.ChoiceField(required=False)

    def clean(self):
        cleaned_data = super(OrderPeriodForm, self).clean()
        min_date = cleaned_data.get("min_date")
        max_date = cleaned_data.get("max_date")

        if min_date and max_date:
            if max_date < min_date:
                raise forms.ValidationError("End time cannot be earlier than start time!")
        return cleaned_data
