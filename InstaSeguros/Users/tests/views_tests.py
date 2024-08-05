from django.test import Client
from django.urls import reverse
from Users.models import User
import pytest


@pytest.mark.django_db
def test_myview_get():
    user1 = User.objects.create(
        name="Rodrigo",
        last_name="Javier",
        birth="1990-01-01",
    )
    user2 = User.objects.create(
        name="Juan",
        last_name="Pedro",
        birth="2000-10-09",
    )

    client = Client()
    response = client.get(reverse("users"))
    assert response.status_code == 200
    response_data = response.json()
    assert "users" in response_data

    assert len(response_data["users"]) == 2
    users_data = response_data["users"]
    assert any(
        user["name"] == user1.name
        and user["last_name"] == user1.last_name
        and user["birth"] == str(user1.birth)
        for user in users_data
    )
    assert any(
        user["name"] == user2.name
        and user["last_name"] == user2.last_name
        and user["birth"] == str(user2.birth)
        for user in users_data
    )
    assert response.json() == {"users": [user1, user2]}


@pytest.mark.django_db
def test_my_view_get_by_id():
    user = User.objects.create(
        name="Rodrigo",
        last_name="Javier",
        birth="1990-01-01",
    )
    client = Client()
    response = client.get(reverse("user_view_param") + f"/{user.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert "user" in response_data
    assert response_data["user"]["name"] == user.name
    assert response_data["user"]["last_name"] == user.last_name
    assert response_data["user"]["birth"] == str(user.birth)


@pytest.mark.django_db
def test_my_view_get_by_id_not_found():
    client = Client()
    response = client.get(reverse("users") + "/999")
    assert response.status_code == 404


@pytest.mark.django_db
def test_my_view_post():
    data = {
        "name": "Rodrigo",
        "last_name": "Javier",
        "birth": "1990-01-01",
    }
    client = Client()
    response = client.post(reverse("user_views"), data)
    assert response.status_code == 200
    response_data = response.json()
    assert "user" in response_data
    user_created = User.objects.get(name=data["name"])
    assert user_created.name == data["name"]
    assert user_created.last_name == data["last_name"]
    assert user_created.birth == data["birth"]


@pytest.mark.django_db
def test_my_view_post_invalid_data():
    data = {
        "name": 1,
        "last_name": None,
        "birth": "Pedro",
    }
    client = Client()
    response = client.post(reverse("user_views"))
    assert response.status_code == 400


@pytest.mark.django_db
def test_my_view_put():
    user = User.objects.create(
        name="Rodrigo",
        last_name="Javier",
        birth="1990-01-01",
    )
    data = {
        "name": "Juan",
        "last_name": "Pedro",
    }
    client = Client()
    response = client.put(reverse("user_view_param") + f"/{user.id}", data)
    assert response.status_code == 200
    user_updated = User.objects.get(id=user.id)
    assert user_updated.name == data["name"]
    assert user_updated.last_name == data["last_name"]


@pytest.mark.django_db
def test_my_view_put_invalid_data():
    user = User.objects.create(
        name="Rodrigo",
        last_name="Javier",
        birth="1990-01-01",
    )
    data = {
        "name": 1,
        "last_name": None,
    }
    client = Client()
    response = client.put(reverse("user_view_param") + f"/{user.id}", data)
    assert response.status_code == 400
