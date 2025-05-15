import requests
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class VerifyRecaptchaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("recaptcha")

        if not token:
            return Response(
                {"success": False, "error": "Missing reCAPTCHA token"}, status=400
            )

        url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": token,
            "remoteip": request.META.get("REMOTE_ADDR"),
        }

        try:
            r = requests.post(url, data=payload, timeout=5)
            result = r.json()
        except requests.exceptions.RequestException:
            return Response(
                {"success": False, "error": "Google verification failed"}, status=500
            )

        if result.get("success"):
            return Response({"success": True})
        return Response(
            {"success": False, "error-codes": result.get("error-codes", [])}, status=400
        )
