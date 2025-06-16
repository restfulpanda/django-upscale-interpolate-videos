import pytest
import uuid
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from authentication.models import User

pytestmark = pytest.mark.django_db


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
