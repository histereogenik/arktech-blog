from rest_framework import serializers

from posts.models import ALLOWED_TAGS, Post


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "subtitle",
            "author",
            "author_name",
            "tags",
            "image",
            "paragraphs",
            "cta",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "author_name", "created_at", "updated_at"]

    def validate_tags(self, value):
        invalid_tags = [tag for tag in value if tag not in ALLOWED_TAGS]
        if invalid_tags:
            raise serializers.ValidationError(f"Invalid tags: {invalid_tags}")
        return value

    def validate_paragraphs(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Paragraphs must be a list.")
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError(
                    "Each paragraph must be a dictionary."
                )
            if "content" not in item:
                raise serializers.ValidationError(
                    "Each paragraph must have a 'content' field."
                )
        return value

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
