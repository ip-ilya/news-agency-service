from django.test import TestCase

from news_agency.forms import (
    RedactorCreationForm,
    RedactorUpdateForm
)


class RedactorCreateAndUpdateFormsTest(TestCase):
    def setUp(self):
        self.creation_form_data = {
            "username": "test",
            "first_name": "test_first",
            "last_name": "test_last",
            "email": "test@test.com",
            "bio": "Some Text",
            "years_of_experience": 1,
            "instagram": "https://www.instagram.com/test_account/",
            "linkedin": "https://www.linkedin.com/in/test-account",
            "twitter": "https://x.com/test_account",
            "facebook": "https://www.facebook.com/testaccount/",
            "password1": "test_password123",
            "password2": "test_password123",
        }
        self.update_form_data = {
            "username": "test",
            "first_name": "test_first",
            "last_name": "test_last",
            "email": "test@test.com",
            "bio": "Some Text",
            "years_of_experience": 1,
            "instagram": "https://www.instagram.com/test_account/",
            "linkedin": "https://www.linkedin.com/in/test-account",
            "twitter": "https://x.com/test_account",
            "facebook": "https://www.facebook.com/testaccount/"
        }

    def test_forms_with_custom_fields_are_valid(self):
        for form, form_data in (
            (RedactorCreationForm, self.creation_form_data),
            (RedactorUpdateForm, self.update_form_data)
        ):
            with self.subTest(form=form):
                filled_form = form(data=form_data)

                self.assertTrue(filled_form.is_valid())
                self.assertEqual(
                    filled_form.cleaned_data,
                    form_data
                )
