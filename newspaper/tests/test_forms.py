from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper.forms import RedactorCreateForm, RedactorUpdateForm


class FormsTests(TestCase):
    def test_redactor_creation_form_with_extra_fields(self):
        form_data = {
            "username": "redactor",
            "password1": "redactorPassword1",
            "password2": "redactorPassword1",
            "first_name": "RED",
            "last_name": "ACTOR",
            "years_of_experience": 10,
        }
        form = RedactorCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(form.cleaned_data["first_name"], form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"], form_data["last_name"])
        self.assertEqual(
            form.cleaned_data["years_of_experience"],
            form_data["years_of_experience"],
        )


    def test_redactor_update_form_with_extra_fields(self):
        form_data = {
            "username": "redactor",
            "password1": "redactorPassword1",
            "password2": "redactorPassword1",
            "first_name": "RED",
            "last_name": "ACTOR",
            "years_of_experience": 10,
        }
        form = RedactorUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(form.cleaned_data["first_name"], form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"], form_data["last_name"])
        self.assertEqual(
            form.cleaned_data["years_of_experience"],
            form_data["years_of_experience"],
        )

    def test_create_redactor(self):
        user = get_user_model().objects.create_user(
            username="redactor1",
            password="redactor",
        )
        self.client.force_login(user)
        form_data = {
            "username": "redactor",
            "email": "redactor@gmail.com",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "first_name": "RED",
            "last_name": "ACTOR",
            "years_of_experience": 10,
        }
        self.client.post(reverse("newspaper:redactor-create"), data=form_data)

        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.years_of_experience, form_data["years_of_experience"])
