from django.core.management.base import BaseCommand
from apps.anime.tasks import fetch_seasonal_anime


class Command(BaseCommand):
    help = "Import Seasonal Anime"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching Seasonal Anime...")
        fetch_seasonal_anime.delay()
        self.stdout.write(
            self.style.SUCCESS("Task submitted.")
        )