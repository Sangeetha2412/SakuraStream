from django.core.management.base import BaseCommand
from django.core.management import call_command
from apps.anime.models import Anime


class Command(BaseCommand):
    help = "Load initial anime data"

    def handle(self, *args, **kwargs):

        if Anime.objects.exists():
            self.stdout.write(self.style.SUCCESS("Anime already loaded."))
            return

        self.stdout.write("Loading genres...")
        call_command("loaddata", "genre")

        self.stdout.write("Loading studios...")
        call_command("loaddata", "studio")

        self.stdout.write("Loading anime...")
        call_command("loaddata", "anime")

        self.stdout.write(self.style.SUCCESS("Anime database imported successfully."))