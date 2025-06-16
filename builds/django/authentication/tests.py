import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer

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
def registered_user(user_data):
    user = User.objects.create_user(**user_data)
    return user


@pytest.fixture
def auth_client(user_data):
    client = APIClient()

    register_response = client.post(
        reverse("authentication:register"), data={"user": user_data}, format="json"
    )
    assert register_response.status_code == status.HTTP_201_CREATED
    assert token_has_access_and_refresh(register_response.data["token"])

    login_response = client.post(
        reverse("authentication:login"),
        data={"user": {"email": user_data["email"], "password": user_data["password"]}},
        format="json",
    )
    assert login_response.status_code == status.HTTP_200_OK

    token = login_response.data["token"]["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    return client, user_data


def test_user_retrieve(auth_client):
    client, user_data = auth_client

    response = client.get(reverse("authentication:get-user"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user_data["email"]
    assert response.data["username"] == user_data["username"]
    assert token_has_access_and_refresh(response.data["token"])


def test_user_update(auth_client):
    client, _ = auth_client

    updated_username = "updateduser"
    response = client.put(
        reverse("authentication:get-user"),
        data={"user": {"username": updated_username}},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == updated_username
    assert token_has_access_and_refresh(response.data["token"])


def test_registration_serializer_valid(user_data):
    serializer = RegistrationSerializer(data=user_data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.email == user_data["email"]
    assert token_has_access_and_refresh(user.token)


def test_login_serializer_valid(registered_user):
    data = {
        "email": registered_user.email,
        "password": "strongpassword123",
    }
    serializer = LoginSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    validated_data = serializer.validated_data
    assert validated_data["email"] == registered_user.email
    assert validated_data["username"] == registered_user.username
    assert token_has_access_and_refresh(validated_data["token"])


def test_login_serializer_invalid(registered_user):
    data = {
        "email": registered_user.email,
        "password": "wrongpassword",
    }
    serializer = LoginSerializer(data=data)
    with pytest.raises(Exception):
        serializer.is_valid(raise_exception=True)


def test_user_serializer_update(registered_user):
    data = {
        "username": "updatedusername",
        "password": "NewStrongPass456",
    }
    serializer = UserSerializer(instance=registered_user, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.username == data["username"]
    assert user.check_password(data["password"])
    assert token_has_access_and_refresh(user.token)
