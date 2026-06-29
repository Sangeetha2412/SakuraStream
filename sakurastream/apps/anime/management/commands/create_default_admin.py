from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = "Create default admin if not exists"

    def handle(self, *args, **kwargs):

        username = getattr(settings, "DEFAULT_ADMIN_USERNAME", "sangeetha")
        email = getattr(settings, "DEFAULT_ADMIN_EMAIL", "yourmail@gmail.com")
        password = getattr(settings, "DEFAULT_ADMIN_PASSWORD", "Sangeetha24")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS("Admin already exists."))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS("Default admin created successfully.")
        )