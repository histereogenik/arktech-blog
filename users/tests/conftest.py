import pytest
from django.urls import reverse


@pytest.fixture
def superuser_token(api_client, create_user):
    superuser = create_user(is_superuser=True, is_staff=True)
    url = reverse("token_obtain_pair")
    response = api_client.post(
        url, {"email": superuser.email, "password": "testpass123"}
    )
    assert response.status_code == 200
    return response.data["access"]


@pytest.fixture
def superuser_client(api_client, superuser_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {superuser_token}")
    return api_client
