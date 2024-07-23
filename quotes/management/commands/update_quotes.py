# quotes/management/commands/update_quotes.py

from django.core.management.base import BaseCommand
from django.db import transaction
from quotes.models import Author, Quote, Tag
import requests
from bs4 import BeautifulSoup
import json

class Command(BaseCommand):
    help = 'Scrapes quotes from the website and updates the database'

    def handle(self, *args, **kwargs):
        # Aquí iría el código del web scraper
        # ...

        # Luego, el código de importación de datos
        with transaction.atomic():
            # Código de importación
            # ...

        self.stdout.write(self.style.SUCCESS('Successfully updated quotes database'))