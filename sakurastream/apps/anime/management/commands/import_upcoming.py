from django.core.management.base import BaseCommand
from apps.anime.tasks import fetch_upcoming_anime


class Command(BaseCommand):
    help = "Import Upcoming Anime"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching Upcoming Anime...")
        fetch_upcoming_anime.delay()
        self.stdout.write(
            self.style.SUCCESS("Task submitted.")
        )