from django.test import Client
from django.urls import reverse
from Users.models import User
import pytest
from Users.factories import UserFactory
import json

client = Client()


@pytest.mark.django_db
def test_myview_get():
    user1 = UserFactory.create()
    user2 = UserFactory.create()
    client = Client()
    response = client.get(reverse("user_view"))
    assert response.status_code == 200

    response_data = response.json()
    assert "users" in response_data

    users = [user1, user2]
    expected_data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "name": user.name,
            "last_name": user.last_name,
            "birth": str(user.birth),
        }
        for user in users
    ]

    # print("User: ", user1.id)
    # print("User: ", user2.id)
    assert response_data["users"] == expected_data


@pytest.mark.django_db
def test_my_view_get_by_id():
    user = UserFactory.create()

    response = client.get(reverse("user_view_param", kwargs={"pk": user.id}))
    assert response.status_code == 200
    response_data = response.json()
    assert "user" in response_data
    assert response_data["user"]["name"] == user.name
    assert response_data["user"]["last_name"] == user.last_name
    assert response_data["user"]["birth"] == str(user.birth)
    print("User: ", user.id)


@pytest.mark.django_db
def test_my_view_get_by_id_not_found():

    response = client.get(reverse("user_view_param", kwargs={"pk": 10}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_my_view_post():
    # Create with factory...
    user_data = {
        "username": "Pedro123456",
        "email": "pedro@gmail.com",
        "password": "1234",
        "name": "Pedro",
        "last_name": "Rodriguez",
        "birth": "2004-09-08",
    }

    response = client.post(
        reverse("user_view"),
        json.dumps(user_data),
        content_type="application/json",
    )
    assert response.status_code == 201
    response_data = response.json()
    assert "user" in response_data
    user_created = User.objects.get(name=user_data["name"])
    assert user_created.name == user_data["name"]
    assert user_created.last_name == user_data["last_name"]
    assert str(user_created.birth) == user_data["birth"]


@pytest.mark.django_db
def test_my_view_post_invalid_data():
    data = {
        "name": 1,
        "last_name": 2,
        "birth": "Pedro",
    }

    response = client.post(reverse("user_view"), data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_my_view_put():
    user = UserFactory.create()
    data = {
        "name": "Juan",
        "last_name": "Pedro",
    }

    response = client.put(
        reverse("user_view_param", kwargs={"pk": user.id}),
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 200
    user_updated = User.objects.get(id=user.id)
    assert user_updated.name == data["name"]
    assert user_updated.last_name == data["last_name"]


@pytest.mark.django_db
def test_my_view_put_invalid_data():
    user = UserFactory.create()
    data = {
        "name": 1,
        "last_name": None,
    }
    client = Client()
    response = client.put(
        reverse("user_view_param", kwargs={"pk": user.id}),
        data=json.dumps(data),
        content_type="application/json",
    )
    print( user)
    assert response.status_code == 400
