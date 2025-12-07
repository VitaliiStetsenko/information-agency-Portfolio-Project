from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from newspaper.models import Topic, Newspaper


class TestModels(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="test")
        self.assertEqual(str(topic), topic.name)

    def test_redactor_str(self):
        redactor = get_user_model().objects.create(
            username="test",
            first_name="test",
            last_name="test",
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username} "
            f"({redactor.first_name} "
            f"{redactor.last_name})"
        )

    def test_newspaper_str(self):
        newspaper = Newspaper.objects.create(
            title="test",
            published=date.today()
        )
        redactor = get_user_model().objects.create(
            username="test",
            first_name="test",
            last_name="test",
        )
        topic = Topic.objects.create(name="test")
        newspaper.topics.add(topic)
        newspaper.publishers.add(redactor)
        self.assertEqual(str(newspaper), newspaper.title)

    def test_create_redactor_with_years_of_experience(self):
        redactor = get_user_model().objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            password="sewwrwrwwffs",
            years_of_experience=9,
        )
        self.assertEqual(redactor.years_of_experience, 9)
        self.assertEqual(redactor.username, "test")
        self.assertTrue(redactor.check_password("sewwrwrwwffs"))
