import pytest
from django.urls import reverse

from users.models import User


@pytest.mark.django_db
class TestUserPermissions:

    def test_superuser_can_create_user(self, api_client, create_user):
        superuser = create_user(is_superuser=True, is_staff=True)
        api_client.force_authenticate(user=superuser)

        url = reverse("user-list")
        data = {
            "email": "newstaff@example.com",
            "username": "newstaff",
            "password": "staffpass123",
        }

        response = api_client.post(url, data)
        assert response.status_code == 201
        assert User.objects.filter(email="newstaff@example.com").exists()

    def test_staff_cannot_create_user(self, api_client, create_user):
        staff = create_user(is_staff=True)
        api_client.force_authenticate(user=staff)

        url = reverse("user-list")
        data = {
            "email": "blockedstaff@example.com",
            "username": "blockedstaff",
            "password": "staffpass123",
        }

        response = api_client.post(url, data)
        assert response.status_code in [403, 401]  # Forbidden or Unauthorized
        assert not User.objects.filter(email="blockedstaff@example.com").exists()

    def test_staff_can_list_users(self, api_client, create_user):
        staff = create_user(is_staff=True)
        api_client.force_authenticate(user=staff)

        url = reverse("user-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_staff_cannot_update_user(self, api_client, create_user):
        staff = create_user(is_staff=True)
        target_user = create_user(email="target@example.com", username="targetuser")
        api_client.force_authenticate(user=staff)

        url = reverse("user-detail", args=[target_user.id])
        data = {"username": "hackedname"}

        response = api_client.patch(url, data)
        assert response.status_code in [403, 401]

    def test_unauthenticated_can_read(self, api_client):
        url = reverse("user-list")
        response = api_client.get(url)
        assert response.status_code == 200
