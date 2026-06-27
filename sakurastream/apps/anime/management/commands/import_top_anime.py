from django.core.management.base import BaseCommand
from apps.anime.tasks import fetch_top_anime


class Command(BaseCommand):
    help = "Import Top Anime from Jikan"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching Top Anime...")
        fetch_top_anime.delay()
        self.stdout.write(
            self.style.SUCCESS("Task submitted.")
        )