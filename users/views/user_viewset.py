from rest_framework import viewsets

from users.models import User
from users.permissions import IsSuperUserOrReadOnly
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrReadOnly]  # Only admin/staff can access
