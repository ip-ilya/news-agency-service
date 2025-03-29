from django.contrib.auth.forms import UserCreationForm
from django import forms

from news_agency.models import Redactor


class RedactorCreationForm(UserCreationForm):
    years_of_experience = forms.IntegerField()

    class Meta:
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("years_of_experience", "first_name", "last_name")


class RedactorUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ("username", "years_of_experience", "first_name", "last_name")
