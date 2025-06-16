import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from .models import User

pytestmark = pytest.mark.django_db

User = get_user_model()

def token_has_access_and_refresh(token):
    return isinstance(token, dict) and "access" in token and "refresh" in token

@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "strongpassword123",
    }


@pytest.fixture
def auth_client(user_data):
    client = APIClient()

    response = client.post(
        reverse("authentication:register"), data={"user": user_data}, format="json"
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert "email" in response.data
    assert response.data["email"] == user_data["email"]
    assert User.objects.filter(email=user_data["email"]).exists()

    login_response = client.post(
        reverse("authentication:login"),
        data={
            "user": {
                "email": user_data["email"],
                "password": user_data["password"],
            }
        },
        format="json",
    )
    assert login_response.status_code == status.HTTP_200_OK
    assert "token" in login_response.data

    token = login_response.data["token"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    return client, user_data


def test_user_retrieve(auth_client):
    client, user_data = auth_client
    response = client.get(reverse("authentication:get-user"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user_data["email"]
    assert response.data["username"] == user_data["username"]


def test_user_update(auth_client):
    client, _ = auth_client
    response = client.put(
        reverse("authentication:get-user"),
        data={"user": {"username": "updateduser"}},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "updateduser"

class RegistrationSerializerTest(TestCase):
    def test_create_user(self):
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "ComplexPass123"
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, data["email"])
        # Assuming token is generated as a dict with refresh and access tokens.
        self.assertTrue(token_has_access_and_refresh(user.token))

class LoginSerializerTest(TestCase):
    def setUp(self):
        self.password = "ComplexPass123"
        self.user = User.objects.create_user(
            email="loginuser@example.com", username="loginuser", password=self.password
        )

    def test_login_valid(self):
        data = {
            "email": self.user.email,
            "password": self.password,
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        validated_data = serializer.validated_data
        self.assertEqual(validated_data.get("email"), self.user.email)
        self.assertEqual(validated_data.get("username"), self.user.username)
        self.assertTrue(token_has_access_and_refresh(validated_data.get("token")))

    def test_login_invalid(self):
        data = {
            "email": self.user.email,
            "password": "WrongPassword",
        }
        serializer = LoginSerializer(data=data)
        with self.assertRaises(Exception):
            serializer.is_valid(raise_exception=True)

class UserSerializerTest(TestCase):
    def setUp(self):
        self.password = "ComplexPass123"
        self.user = User.objects.create_user(
            email="updateuser@example.com", username="updateuser", password=self.password
        )

    def test_update_password_and_username(self):
        new_password = "NewComplexPass456"
        new_username = "updatedusername"
        data = {
            "username": new_username,
            "password": new_password,
        }
        serializer = UserSerializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, new_username)
        self.assertTrue(updated_user.check_password(new_password))
        self.assertTrue(token_has_access_and_refresh(updated_user.token))
        