from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from news_agency.models import Topic, Redactor, Newspaper

LOGIN_URL = reverse("login")
INDEX_URL = reverse("news_agency:index")

# ALL TOPIC URLS:
TOPIC_LIST_URL = reverse("news_agency:topic-list")
TOPIC_CREATE_URL = reverse("news_agency:topic-create")


def get_topic_detail_url(topic: Topic):
    return reverse(
        "news_agency:topic-detail",
        kwargs={"pk": topic.pk}
    )


def get_topic_update_url(topic: Topic):
    return reverse(
        "news_agency:topic-update",
        kwargs={"pk": topic.pk}
    )


def get_topic_delete_url(topic: Topic):
    return reverse(
        "news_agency:topic-delete",
        kwargs={"pk": topic.pk}
    )


# ALL REDACTOR URLS
REDACTOR_LIST_URL = reverse("news_agency:redactor-list")
REDACTOR_CREATE_URL = reverse("news_agency:redactor-create")


def get_redactor_detail_url(redactor: Redactor):
    return reverse(
        "news_agency:redactor-detail",
        kwargs={"pk": redactor.pk}
    )


def get_redactor_update_url(redactor: Redactor):
    return reverse(
        "news_agency:redactor-update",
        kwargs={"pk": redactor.pk}
    )


def get_redactor_delete_url(redactor: Redactor):
    return reverse(
        "news_agency:redactor-delete",
        kwargs={"pk": redactor.pk}
    )


# ALL NEWSPAPER URLS:
NEWSPAPER_LIST_URL = reverse("news_agency:newspaper-list")
NEWSPAPER_CREATE_URL = reverse("news_agency:newspaper-create")


def get_newspaper_detail_url(newspaper: Newspaper):
    return reverse(
        "news_agency:newspaper-detail",
        kwargs={"pk": newspaper.pk}
    )


def get_newspaper_update_url(newspaper: Newspaper):
    return reverse(
        "news_agency:newspaper-update",
        kwargs={"pk": newspaper.pk}
    )


def get_newspaper_delete_url(newspaper: Newspaper):
    return reverse(
        "news_agency:newspaper-delete",
        kwargs={"pk": newspaper.pk}
    )


SEARCH_PARAMETERS = ("1", "2", "3")


class LoginRequiredMixinTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test-username",
            password="test-password",
            years_of_experience=1
        )
        cls.newspaper = Newspaper.objects.create(
            title="Test title",
            content="Test content"
        )

    def test_public_access_redirect(self):
        for url in (
                NEWSPAPER_CREATE_URL,
                get_newspaper_update_url(self.newspaper),
                get_newspaper_delete_url(self.newspaper),
                get_redactor_update_url(self.user),
                get_redactor_delete_url(self.user)
        ):
            response = self.client.get(url)
            with self.subTest(url=url):
                self.assertEqual(
                    response.status_code,
                    302
                )
                self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_private_access_allowed(self):
        self.client.force_login(self.user)
        for url in (
                NEWSPAPER_CREATE_URL,
                get_redactor_update_url(self.user),
                get_redactor_delete_url(self.user)
        ):
            response = self.client.get(url)
            with self.subTest(url=url):
                self.assertTrue(
                    response.status_code,
                    200
                )
                print(response.status_code)

    def test_private_access_restricted(self):
        self.client.force_login(self.user)
        for url in (
                get_newspaper_update_url(self.newspaper),
                get_newspaper_delete_url(self.newspaper),
        ):
            response = self.client.get(url)
            with self.subTest(url=url):
                self.assertEqual(
                    response.status_code,
                    403
                )


class AdminRequiredMixinTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff_user = get_user_model().objects.create_user(
            username="admin",
            password="adminpassword",
            years_of_experience=1,
            email="admin@admin.com",
            is_staff=True
        )

        cls.default_user = get_user_model().objects.create_user(
            username="user",
            password="userpassword",
            years_of_experience=1,
            email="user@user.com"
        )

        cls.topic = Topic.objects.create(name="test")
        cls.urls = [
            get_topic_update_url(cls.topic),
            get_topic_delete_url(cls.topic),
            TOPIC_CREATE_URL,
            REDACTOR_CREATE_URL
        ]

    def test_admin_user_access_allowed(self):
        self.client.force_login(self.staff_user)
        for url in self.urls:
            response = self.client.get(url)
            with self.subTest(url=url):
                self.assertEqual(
                    response.status_code,
                    200
                )

    def test_default_user_access_restricted(self):
        self.client.force_login(self.default_user)
        for url in self.urls:
            response = self.client.get(url)
            with self.subTest(url=url):
                self.assertEqual(
                    response.status_code,
                    403
                )


class UserPassesCustomTestMixinTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.staff_user = get_user_model().objects.create_user(
            username="admin",
            password="adminpassword",
            years_of_experience=1,
            email="admin@admin.com",
            is_staff=True
        )
        cls.newspaper_creator = get_user_model().objects.create_user(
            username="newspaper_creator",
            password="userpassword",
            years_of_experience=1,
            email="user@user.com"
        )
        cls.other_user = get_user_model().objects.create_user(
            username="random_user",
            password="randompassword",
            years_of_experience=1,
            email="random@random.com"
        )
        cls.newspaper = Newspaper.objects.create(
            title="Test title",
            content="Test content"
        )
        cls.newspaper.publishers.add(cls.newspaper_creator)

        cls.urls = [
            get_newspaper_update_url(cls.newspaper),
            get_newspaper_delete_url(cls.newspaper),
            get_redactor_update_url(cls.newspaper_creator),
            get_redactor_delete_url(cls.newspaper_creator),
        ]

    @classmethod
    def tearDownClass(cls):
        pass

    def test_access_allowed_for_object_creator(self):
        self.client.force_login(self.newspaper_creator)
        for url in self.urls:
            response = self.client.get(url)
            with self.subTest(url=url):
                self.assertEqual(response.status_code, 200)

    def test_access_allowed_for_staff(self):
        self.client.force_login(self.staff_user)
        for url in self.urls:
            response = self.client.get(url)
            with self.subTest(url=url):
                self.assertEqual(response.status_code, 200)

    def test_access_restricted_for_other_users(self):
        self.client.force_login(self.other_user)
        for url in self.urls:
            response = self.client.get(url)
            with self.subTest(user=self.other_user, url=url):
                self.assertEqual(response.status_code, 403)


class IndexTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="user",
            password="password",
            years_of_experience=1,
            email="admin@admin.com"
        )
        topic = Topic.objects.create(name="test")
        newspaper = Newspaper.objects.create(
            title="Some Title",
            content="Some Content"
        )
        newspaper.topics.add(topic)
        newspaper.publishers.add(cls.user)

    def test_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get(INDEX_URL)
        for object_name in ("num_topics", "num_redactors", "num_newspapers"):
            with self.subTest(object_name=object_name):
                self.assertEqual(
                    response.context[object_name],
                    1
                )


class NewspaperCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="user",
            password="password",
            years_of_experience=1,
            email="user@user.com"
        )
        cls.topic = Topic.objects.create(name="test")

    def test_form_valid_view_assign_user_to_newspaper_publishers(self):
        self.client.force_login(self.user)
        response = self.client.post(
            NEWSPAPER_CREATE_URL,
            data={
                "title": "Some Title",
                "content": "Some Content",
                "topics": [self.topic.pk]
            }
        )
        newspaper = Newspaper.objects.first()
        newspaper_publishers = newspaper.publishers.all()

        self.assertTrue(response.status_code, 302)
        self.assertEqual(response.url, get_newspaper_detail_url(newspaper))
        self.assertTrue(
            self.user in newspaper_publishers
        )


class TestCustomLoginView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="user",
            password="password",
            years_of_experience=1,
            email="user@user.com"
        )

    def test_login_view_redirects_to_index_page_authenticated_users(self):
        self.client.force_login(self.user)
        response = self.client.get(LOGIN_URL)
        self.assertTrue(
            response.url,
            INDEX_URL
        )


class RedactorSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="user 1",
            password="password",
            years_of_experience=1,
            email="user@user.com"
        )
        cls.another_user = get_user_model().objects.create_user(
            username="user 2",
            password="password",
            years_of_experience=1,
            email="user2@user.com"
        )

    def test_by_username(self):
        for username in SEARCH_PARAMETERS:
            with self.subTest(username=username):
                response = self.client.get(
                    REDACTOR_LIST_URL,
                    {"username": username}
                )
                self.assertEqual(
                    list(get_user_model().objects.filter(
                        username__icontains=username)
                    ),
                    list(response.context["redactor_list"])
                )


class TopicSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.topic = Topic.objects.create(name="topic 1")
        cls.topic_2 = Topic.objects.create(name="topic 2")

    def test_by_name(self):
        for name in SEARCH_PARAMETERS:
            with self.subTest(name=name):
                response = self.client.get(
                    TOPIC_LIST_URL,
                    {"name": name}
                )
                self.assertEqual(
                    list(Topic.objects.filter(name__icontains=name)),
                    list(response.context["topic_list"])
                )


class NewspaperSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.newspaper = Newspaper.objects.create(
            title="Title 1",
            content="Content 1"
        )
        cls.newspaper_2 = Newspaper.objects.create(
            title="Title 2",
            content="Content 2"
        )

    def test_by_name(self):
        for title in SEARCH_PARAMETERS:
            with self.subTest(title=title):
                response = self.client.get(
                    NEWSPAPER_LIST_URL,
                    {"title": title}
                )
                self.assertEqual(
                    list(Newspaper.objects.filter(title__icontains=title)),
                    list(response.context["newspaper_list"])
                )
