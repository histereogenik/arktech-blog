import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
import uuid

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        unique_suffix = uuid.uuid4().hex[:8]
        defaults = {
            'email': f'testuser_{unique_suffix}@example.com',
            'username': f'testuser_{unique_suffix}',
            'password': 'testpass123'
        }
        defaults.update(kwargs)
        user = User.objects.create_user(**defaults)
        return user
    return make_user

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_token(api_client, create_user):
    user = create_user(is_staff=True)
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {'email': user.email, 'password': 'testpass123'})
    assert response.status_code == 200
    return response.data['access']

@pytest.fixture
def auth_client(api_client, admin_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
    return api_client