from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seed the database with users'

    def handle(self, *args, **kwargs):
        # Menambahkan beberapa user
        users = [
            {'username': 'admin', 'password': 'admin123'},
        ]

        for user_data in users:
            # Memastikan user tidak duplikat
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    password=user_data['password'],
                )
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User {user.username} created successfully"))
            else:
                self.stdout.write(self.style.WARNING(f"User {user_data['username']} already exists"))
