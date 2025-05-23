import shutil
import uuid

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User


# Temporary media root for file uploads
@pytest.fixture(autouse=True)
def temp_media_root(tmp_path, settings):
    temp_dir = tmp_path / "media"
    temp_dir.mkdir()
    settings.MEDIA_ROOT = str(temp_dir)
    yield
    shutil.rmtree(str(temp_dir))


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        unique_suffix = uuid.uuid4().hex[:8]
        defaults = {
            "email": f"testuser_{unique_suffix}@example.com",
            "username": f"testuser_{unique_suffix}",
            "password": "testpass123",
        }
        defaults.update(kwargs)
        user = User.objects.create_user(**defaults)
        return user

    return make_user


@pytest.fixture
def admin_token(api_client, create_user):
    user = create_user(is_staff=True)
    url = reverse("token_obtain_pair")
    response = api_client.post(url, {"email": user.email, "password": "testpass123"})
    assert response.status_code == 200
    return response.data["access"]


@pytest.fixture
def auth_client(api_client, admin_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    return api_client
