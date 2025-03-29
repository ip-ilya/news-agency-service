from django.contrib.auth.forms import UserCreationForm
from django import forms

from news_agency.models import Redactor


class RedactorCreationForm(UserCreationForm):
    years_of_experience = forms.IntegerField()

    class Meta:
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "bio",
            "years_of_experience",
            "instagram",
            "linkedin",
            "twitter",
            "facebook"
        )


class RedactorUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "bio",
            "years_of_experience",
            "instagram",
            "linkedin",
            "twitter",
            "facebook"
        )


class TopicNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class RedactorUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username"
            }
        )

    )


class NewspaperTitleSearchForm(forms.Form):
    title = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by title"
            }
        )

    )
