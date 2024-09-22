from django.test import TestCase

from storage.forms import UserCreateForm


class FormsTests(TestCase):
    def test_user_createion_with_occupation_first_last_name_is_valid(self):
        form_data = {
            "username": "user",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "First",
            "last_name": "Last",
            "occupation": "City",
        }
        form = UserCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
