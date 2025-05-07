import pytest
from users.serializers import UserSerializer
from users.models import User

@pytest.mark.django_db
def test_user_serializer_output(create_user):
    user = create_user()
    serializer = UserSerializer(user)
    data = serializer.data

    assert data['email'] == user.email
    assert data['username'] == user.username
    assert 'id' in data
    assert 'avatar' in data
