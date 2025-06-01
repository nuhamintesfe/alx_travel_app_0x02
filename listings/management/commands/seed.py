from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        # Optional: clear existing listings
        Listing.objects.all().delete()

        # Create sample users (if none exist)
        if not User.objects.exists():
            User.objects.create_user(username='user1', password='pass123')
            User.objects.create_user(username='user2', password='pass123')

        users = list(User.objects.all())

        for i in range(10):  # Create 10 sample listings
            listing = Listing.objects.create(
                title=f"Sample Listing {i+1}",
                description="This is a sample description for listing.",
                price_per_night=random.uniform(50, 200),
                address=f"{i+1} Example St, Sample City",
                owner=random.choice(users),
            )
            self.stdout.write(self.style.SUCCESS(f'Created listing {listing.title}'))
