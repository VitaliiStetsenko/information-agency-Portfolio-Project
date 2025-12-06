from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from newspaper.forms import (NewspaperSearchForm,
                             TopicSearchForm,
                             RedactorSearchForm)
from newspaper.models import Topic, Newspaper


class TestValidSearchForm(TestCase):
    def test_newspaper_form_valid(self):
        form = NewspaperSearchForm(
            data={
                "title": "Test",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Test")

    def test_topic_form_valid(self):
        form = TopicSearchForm(
            data={
                "name": "Test",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test")

    def test_redactor_form_valid(self):
        form = RedactorSearchForm(
            data={
                "username": "Test",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "Test")


class TestSearchForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Vitalii",
            password="testpassword",
            years_of_experience=1,
        )
        self.client = Client()
        self.client.force_login(self.user)

        self.user2 = get_user_model().objects.create_user(
            username="Vladislav",
            password="testpassword",
            years_of_experience=1,
        )

        self.topic = Topic.objects.create(
            name="Drama",
        )
        self.topic2 = Topic.objects.create(
            name="Comedy",
        )

        self.newspaper = Newspaper.objects.create(
            title="News",
            published=date.today(),
        )
        self.newspaper.topics.add(self.topic)
        self.newspaper.publishers.add(self.user)

        self.newspaper2 = Newspaper.objects.create(
            title="How to cook",
            published=date.today(),
        )
        self.newspaper2.topics.add(self.topic2)
        self.newspaper2.publishers.add(self.user2)

    def test_redactor_search(self):
        url = reverse("newspaper:redactor-list") + "?username=S"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.context["redactor_list"]

        self.assertIn(self.user2, result)
        self.assertNotIn(self.user, result)
        self.assertEqual(len(result), 1)

    def test_topic_search(self):
        url = reverse("newspaper:topic-list") + "?name=Y"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.context["topic_list"]

        self.assertIn(self.topic2, result)
        self.assertNotIn(self.topic, result)
        self.assertEqual(len(result), 1)

    def test_newspaper_search(self):
        url = reverse("newspaper:newspaper-list") + "?title=S"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.context["newspaper_list"]

        self.assertIn(self.newspaper, result)
        self.assertNotIn(self.newspaper2, result)
        self.assertEqual(len(result), 1)
