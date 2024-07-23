# quotes/management/commands/data_import.py

from django.core.management.base import BaseCommand
from quotes.models import Author, Quote, Tag
import json

class Command(BaseCommand):
    help = 'Imports quotes data from JSON file to the database'

    def handle(self, *args, **options):
        with open('quotes_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Import authors
        for author_name, about in data['authors'].items():
            Author.objects.get_or_create(name=author_name, defaults={'about': about})

        # Import quotes and tags
        for quote_data in data['quotes']:
            author = Author.objects.get(name=quote_data['author'])
            quote = Quote.objects.create(text=quote_data['text'], author=author)

            for tag_name in quote_data['tags']:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)

        self.stdout.write(self.style.SUCCESS(f"Imported {len(data['quotes'])} quotes and {len(data['authors'])} authors to the database."))