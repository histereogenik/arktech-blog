from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        import os

        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError

        # ONLY run in development/testing, NOT in production
        if os.getenv("DJANGO_ENV") == "development":
            User = get_user_model()
            try:
                if not User.objects.filter(is_superuser=True).exists():
                    User.objects.create_superuser(
                        email="admin@arktech.com",
                        username="admin",
                        password="AdminTest123!",
                    )
                    print(
                        "Temporary superuser created: admin@arktech.com / AdminTest123!"
                    )
            except OperationalError:
                # Happens during migrations or first boot; safe to ignore
                pass
