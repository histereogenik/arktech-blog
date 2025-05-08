import pytest
from posts.models import Post

@pytest.fixture
def create_post(db, create_user):
    def make_post(**kwargs):
        user = kwargs.pop('author', None) or create_user(is_staff=True)
        defaults = {
            'title': 'Sample Post',
            'subtitle': 'Sample Subtitle',
            'author': user,
            'tags': ['Software Development'],
            'paragraphs': [
                {'title': 'Intro', 'content': 'This is the intro.'},
                {'title': 'Main', 'content': 'This is the main content.'}
            ],
            'cta': 'Click [here](https://example.com)'
        }
        defaults.update(kwargs)
        return Post.objects.create(**defaults)
    return make_post
