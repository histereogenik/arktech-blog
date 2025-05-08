import pytest


@pytest.mark.django_db
def test_user_str(create_user):
    user = create_user()
    assert str(user) == user.email


@pytest.mark.django_db
def test_user_unique_email(create_user, django_db_blocker):
    user1 = create_user()
    with pytest.raises(Exception):
        with django_db_blocker.unblock():
            create_user(email=user1.email)
