from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer
from django.contrib.auth.models import User
import json


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def createSong(title="", artist=""):
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)

    def login_client(self, username="", password=""):
        response = self.client.post(reverse('create-token'), data=json.dumps({
            'username': username,
            'password': password
        }), content_type="application/json")

        self.token = response.data['token']
        # set token in header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

    def login_a_user(self, username="", password=""):
        url = reverse("auth-login", kwargs={"version": "v1"})
        return self.client.post(url, data=json.dumps({
            "username": username,
            "password": password
        }), content_type="application/json")

    def setUp(self):
        # create a test user
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@gmail.com",
            password="tester",
            first_name="test",
            last_name="user",
        )

        self.createSong(title="like glue", artist="sean paul")
        self.createSong(title="simple song", artist="konshens")
        self.createSong(title="love is wicked", artist="brick and lace")
        self.createSong(title="jam rock", artist="damien marley")


class AuthLoginUserTest(BaseViewTest):
    def test_login_user(self):
        response = self.login_a_user('test_user', 'tester')
        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.login_a_user("anonymous", "pass")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetAllSongs(BaseViewTest):
    def test_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        self.login_client('test_user', 'tester')

        response = self.client.get(reverse("songs-all", kwargs={"version": "v1"}))
        expexted = Songs.objects.all()
        serialized = SongsSerializer(expexted, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthRegisterUserTest(BaseViewTest):
    """
    Tests for auth/register/ endpoint
    """

    def test_register_a_user_with_valid_data(self):
        url = reverse("auth-register", kwargs={"version": "v1"})
        response = self.client.post(url, data=json.dumps({
            "username": "new_user",
            "password": "new_pass",
            "email": "new_user@gmail.com"
        }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_a_user_with_invalid_data(self):
        url = reverse("auth-register", kwargs={"version": "v1"})
        response = self.client.post(url, data=json.dumps({
            "username": "",
            "password": "",
            "email": ""
        }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
