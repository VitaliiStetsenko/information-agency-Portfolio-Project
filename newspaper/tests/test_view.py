from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class PublicListViewTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("newspaper:index"))
        self.assertEqual(res.status_code, 200)

    def test_public_newspaper_list(self):
        res = self.client.get(reverse("newspaper:newspaper-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_public_topic_list(self):
        res = self.client.get(reverse("newspaper:topic-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_public_redactor_list(self):
        res = self.client.get(reverse("newspaper:redactor-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            password="sewwrwrwwffs",
            years_of_experience=9,
        )
        self.client.force_login(self.user)

    def test_private_newspaper_list(self):
        res = self.client.get(reverse("newspaper:newspaper-list"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "newspaper/newspaper_list.html")

    def test_private_topic_list(self):
        res = self.client.get(reverse("newspaper:topic-list"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "newspaper/topic_list.html")

    def test_private_redactor_list(self):
        res = self.client.get(reverse("newspaper:redactor-list"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "newspaper/redactor_list.html")
