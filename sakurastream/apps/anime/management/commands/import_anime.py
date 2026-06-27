from django.core.management.base import BaseCommand
from apps.anime.service import import_anime_from_jikan


class Command(BaseCommand):
    help = "Import one anime using MAL ID"

    def add_arguments(self, parser):
        parser.add_argument("mal_id", type=int)

    def handle(self, *args, **options):
        anime, created = import_anime_from_jikan(options["mal_id"])

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Imported {anime.title}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Updated {anime.title}")
            )