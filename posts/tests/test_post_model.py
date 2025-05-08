import pytest
from posts.models import ALLOWED_TAGS

@pytest.mark.django_db
def test_post_str(create_post):
    post = create_post()
    assert str(post) == post.title

@pytest.mark.django_db
def test_post_tags_validation(create_post):
    valid_post = create_post(tags=['Cybersecurity'])
    assert 'Cybersecurity' in valid_post.tags

    # Simulate invalid tag check
    invalid_post = create_post(tags=['InvalidTag'])
    try:
        invalid_post.clean()
    except ValueError as e:
        assert str(e) == "Invalid tag: InvalidTag"
    else:
        assert False, "Expected ValueError for invalid tag"

@pytest.mark.django_db
def test_post_paragraphs_structure(create_post):
    post = create_post()
    assert isinstance(post.paragraphs, list)
    assert all('title' in p and 'content' in p for p in post.paragraphs)
