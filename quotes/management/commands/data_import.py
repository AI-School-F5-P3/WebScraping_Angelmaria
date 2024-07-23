# quotes/management/commands/data_import.py

from django.core.management.base import BaseCommand
from quotes.models import Author, Quote, Tag
from django.db import transaction
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Imports quotes data from JSON file to the database'

    def handle(self, *args, **options):
        try:
            with open('quotes_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            with transaction.atomic():
                self.import_authors(data['authors'])
                self.import_quotes(data['quotes'])

            self.stdout.write(self.style.SUCCESS(f"Imported {len(data['quotes'])} quotes and {len(data['authors'])} authors to the database."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Error: quotes_data.json file not found."))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Error: Invalid JSON in quotes_data.json."))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"Error: Missing key in JSON data: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))

    def import_authors(self, authors_data):
        for author_name, author_info in authors_data.items():
            try:
                Author.objects.update_or_create(
                    name=author_name,
                    defaults={
                        'about': author_info['about'],
                        'born': datetime.strptime(author_info['born'], '%B %d, %Y').date(),
                        'birth_place': author_info['birth_place']
                    }
                )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to import author {author_name}: {str(e)}"))

    def import_quotes(self, quotes_data):
        for quote_data in quotes_data:
            try:
                author = Author.objects.get(name=quote_data['author'])
                quote, created = Quote.objects.get_or_create(
                    text=quote_data['text'],
                    author=author
                )
                if created:
                    for tag_name in quote_data['tags']:
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        quote.tags.add(tag)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to import quote: {str(e)}"))