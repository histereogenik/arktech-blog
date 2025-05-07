import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_user_list_authenticated(create_user):
    user = create_user(is_staff=True)
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('user-list')
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)

@pytest.mark.django_db
def test_user_list_unauthenticated():
    client = APIClient()
    url = reverse('user-list')
    response = client.get(url)

    assert response.status_code == 403  # IsAdminUser blocks unauthenticated
