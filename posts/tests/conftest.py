import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from posts.models import Post


@pytest.fixture
def create_post(db, create_user):
    def make_post(**kwargs):
        user = kwargs.pop("author", None) or create_user(is_staff=True)
        defaults = {
            "title": "Sample Post",
            "subtitle": "Sample Subtitle",
            "author": user,
            "tags": ["Software Development"],
            "paragraphs": [
                {"title": "Intro", "content": "This is the intro."},
                {"title": "Main", "content": "This is the main content."},
            ],
            "cta": "Click [here](https://example.com)",
        }
        defaults.update(kwargs)
        return Post.objects.create(**defaults)

    return make_post


@pytest.fixture
def post_payload():
    return {
        "title": "Sample Post",
        "subtitle": "Sample Subtitle",
        "tags": ["Software Development"],
        "paragraphs": [
            {"title": "Intro", "content": "This is the intro."},
            {"content": "This is the main content without title."},
        ],
        "cta": "Click [here](https://example.com)",
    }


@pytest.fixture
def mock_image():
    file = io.BytesIO()
    image = Image.new("RGB", (100, 100))
    image.save(file, "JPEG")
    file.name = "test_image.jpg"
    file.seek(0)
    return SimpleUploadedFile(file.name, file.read(), content_type="image/jpeg")
