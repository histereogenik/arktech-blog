import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User

@pytest.mark.django_db
def test_user_list_authenticated(create_user):
    user = create_user(is_staff=True)
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('user-list')
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)  # IsAdminUser blocks unauthenticated

@pytest.mark.django_db
class TestUserAPI:

    def test_list_users(self, auth_client):
        url = reverse('user-list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_retrieve_user(self, auth_client, create_user):
        user = create_user(email='other@example.com')
        url = reverse('user-detail', args=[user.id])
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response.data['email'] == user.email

    def test_create_user(self, superuser_client):
        url = reverse('user-list')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpass123'
        }
        response = superuser_client.post(url, data)
        assert response.status_code == 201
        assert User.objects.filter(email='newuser@example.com').exists()

    def test_update_user(self, superuser_client, create_user):
        user = create_user(email='tochange@example.com')
        url = reverse('user-detail', args=[user.id])
        data = {'username': 'updatedname'}
        response = superuser_client.patch(url, data)
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.username == 'updatedname'

    def test_delete_user(self, superuser_client, create_user):
        user = create_user(email='todelete@example.com')
        url = reverse('user-detail', args=[user.id])
        response = superuser_client.delete(url)
        assert response.status_code == 204
        assert not User.objects.filter(id=user.id).exists()
