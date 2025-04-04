from django.contrib.auth import get_user_model
from django.test import TestCase

from news_agency.models import Topic, Newspaper


class Tests(TestCase):
    def setUp(self):
        self.redactor_data = {
            "username": "test",
            "password": "test_password123",
            "first_name": "test_first",
            "last_name": "test_last",
            "email": "test@test.com",
            "years_of_experience": 1,
            "instagram": "https://www.instagram.com/test_account/",
            "linkedin": "https://www.linkedin.com/in/test-account",
            "twitter": "https://x.com/test_account",
            "facebook": "https://www.facebook.com/testaccount/"
        }

    def test_topic_str(self):
        topic = Topic.objects.create(name="test")
        self.assertEqual(str(topic), topic.name)

    def test_redactor_str(self):
        redactor = get_user_model().objects.create_user(
            username=self.redactor_data["username"],
            password=self.redactor_data["password"],
            years_of_experience=self.redactor_data["years_of_experience"]
        )
        self.assertEqual(str(redactor), redactor.username)

    def test_newspaper_str(self):
        newspaper = Newspaper.objects.create(
            title="test title",
            content="test content"
        )
        self.assertEqual(str(newspaper), newspaper.title)

    def test_create_redactor_with_custom_fields(self):
        redactor = get_user_model().objects.create_user(
            username=self.redactor_data["username"],
            password=self.redactor_data["password"],
            first_name=self.redactor_data["first_name"],
            last_name=self.redactor_data["last_name"],
            email=self.redactor_data["email"],
            years_of_experience=self.redactor_data["years_of_experience"],
            instagram=self.redactor_data["instagram"],
            linkedin=self.redactor_data["linkedin"],
            twitter=self.redactor_data["twitter"],
            facebook=self.redactor_data["facebook"]
        )
        self.assertEqual(
            redactor.first_name,
            self.redactor_data["first_name"]
        )
        self.assertEqual(
            redactor.last_name,
            self.redactor_data["last_name"]
        )
        self.assertEqual(
            redactor.email,
            self.redactor_data["email"]
        )
        self.assertEqual(
            redactor.years_of_experience,
            self.redactor_data["years_of_experience"]
        )
        self.assertEqual(
            redactor.instagram,
            self.redactor_data["instagram"]
        )
        self.assertEqual(
            redactor.linkedin,
            self.redactor_data["linkedin"]
        )
        self.assertEqual(
            redactor.twitter,
            self.redactor_data["twitter"]
        )
        self.assertEqual(
            redactor.facebook,
            self.redactor_data["facebook"]
        )
