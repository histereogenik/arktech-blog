from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "avatar", "is_staff", "password"]
        read_only_fields = ["id", "is_staff"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data["is_staff"] = True  # Force all API-created users to be staff

        user = User.objects.create_user(password=password, **validated_data)
        user.is_active = True
        user.save()
        return user
