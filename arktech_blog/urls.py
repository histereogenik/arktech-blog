from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from common.views import VerifyRecaptchaView

urlpatterns = [
    path("api/", include("users.urls")),
    path("api/", include("posts.urls")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/verify-recaptcha/", VerifyRecaptchaView.as_view(), name="verify-recaptcha"
    ),
    path("admin/", admin.site.urls),
]
