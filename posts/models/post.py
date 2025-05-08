from django.core.validators import FileExtensionValidator
from django.db import models

from users.models import User

# Hardcoded allowed tags
ALLOWED_TAGS = [
    "Digital Transformation",
    "Software Development",
    "Cybersecurity",
    "Artificial Intelligence",
    "Cloud Computing",
    "Data Analytics",
    "Technology Trends",
]


class Post(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = models.JSONField(default=list, blank=True)  # list of strings
    image = models.ImageField(
        upload_to="post_images/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )
    paragraphs = models.JSONField(
        default=list, blank=True
    )  # [{title: "", content: ""}, ...]
    cta = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        for tag in self.tags:
            if tag not in ALLOWED_TAGS:
                raise ValueError(f"Invalid tag: {tag}")

    def __str__(self):
        return self.title
