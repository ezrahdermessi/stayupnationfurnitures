from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Create or reset admin user'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = "admin"
        email = "stayupnation129@gmail.com"
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "Admin123!")

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Password reset for {username}"))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser {username} created"))
