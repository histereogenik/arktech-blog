import pytest
from users.models import User

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        defaults = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }
        defaults.update(kwargs)
        user = User.objects.create_user(**defaults)
        return user
    return make_user
