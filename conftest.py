import pytest
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