from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from accounts.models import RegisterableEmail

User = get_user_model()

class Command(BaseCommand):
    help = "Réinitialise la base de données et la remplit avec des données de test"

    def handle(self, *args, **kwargs):
        self.stdout.write("Réinitialisation de la base de données...")

        call_command("flush", "--no-input")

        call_command("migrate")

        self.stdout.write(self.style.SUCCESS("Base de données réinitialisée !"))

        self.stdout.write("Ecriture des données de test")

        # Exemple : créer un admin
        User.objects.create_superuser(
            username="admin",
            email="admin@cocomail.com",
            password="admin",
            first_name = "Admin",
            last_name = "Root",
            verified = True
        )
        User.objects.create_user(
            username="alice",
            email="alice@cocomail.com",
            password="alice",
            first_name = "Alice",
            last_name = "Coco",
            verified = True
        )
        User.objects.create_user(
            username="bob",
            email="bob@cocomail.com",
            password="bob",
            first_name = "Bob",
            last_name = "Coco",
            verified = True
        )

        EMAILS = [
            "admin@cocomail.com",
            "alice@cocomail.com",
            "bob@cocomail.com",
            "cindy@cocomail.com",
            "david@cocomail.com",
            "elena@cocomail.com",
            "fabien@cocomail.com",
        ]
        RegisterableEmail.objects.bulk_create(list(map(lambda email:RegisterableEmail(email=email), EMAILS)))

        self.stdout.write(self.style.SUCCESS("Base de données créée !"))