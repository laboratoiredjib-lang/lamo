import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Crée (ou met à jour le mot de passe d'un) compte administrateur à partir des "
        "variables d'environnement DJANGO_SUPERUSER_USERNAME / _EMAIL / _PASSWORD. "
        "Idempotent : ne fait rien si ces variables ne sont pas définies."
    )

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            self.stdout.write("DJANGO_SUPERUSER_USERNAME/PASSWORD non définis, étape ignorée.")
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username, defaults={"email": email, "is_staff": True, "is_superuser": True}
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Compte administrateur '{username}' créé."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Compte administrateur '{username}' mis à jour."))
