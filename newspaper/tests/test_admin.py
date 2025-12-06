from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="testadmin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="testredactor",
            password="testredactor",
            years_of_experience=2,
        )

    def test_redactor_years_of_experience_listed(self):
        url = reverse("admin:newspaper_redactor_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.redactor.years_of_experience)

    def test_redactor_years_of_experience_detail(self):
        url = reverse(
            "admin:newspaper_redactor_change",
            args=[self.redactor.id,]
        )
        res = self.client.get(url)
        self.assertContains(res, self.redactor.years_of_experience)

    def test_redactor_add_fieldsets(self):
        url = reverse("admin:newspaper_redactor_add",)
        res = self.client.get(url)

        self.assertContains(res, "Additional info")
        self.assertContains(res, "id_first_name")
        self.assertContains(res, "id_last_name")
        self.assertContains(res, "id_years_of_experience")
