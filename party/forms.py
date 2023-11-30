import datetime

from crispy_forms.helper import FormHelper
from django import forms
from django.urls import reverse_lazy

from .models import Party, Gift


class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ("party_date", "party_time", "venue", "invitation")
        widgets = {
            "party_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "hx-get": reverse_lazy("partial_check_party_date"),
                    "hx-trigger": "blur",
                    "hx-swap": "outerHTML",
                    "hx-target": "#div_id_party_date",
                }
            ),
            "party_time": forms.TimeInput(attrs={"type": "time"}),
            "invitation": forms.Textarea(
                attrs={
                    "rows": 10,
                    "cols": 30,
                    "hx-get": reverse_lazy("partial_check_invitation"),
                    "hx-trigger": "blur",
                    "hx-swap": "outerHTML",
                    "hx-target": "#div_id_invitation",
                }
            ),
        }

    def clean_invitation(self):
        invitation = self.cleaned_data["invitation"]

        if len(invitation) < 10:
            raise forms.ValidationError("You really should write an invitation.")

        return invitation

    def clean_party_date(self):
        party_date = self.cleaned_data["party_date"]

        if datetime.date.today() > party_date:
            raise forms.ValidationError("You chose a date in the past.")

        return party_date


class GiftForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Gift
        fields = ("gift", "price", "link")
