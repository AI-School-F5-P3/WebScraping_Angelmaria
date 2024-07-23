# quotes/management/commands/update_quotes.py

from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Updates quotes by scraping the website and importing to the database'

    def handle(self, *args, **options):
        self.stdout.write('Starting web scraping process...')
        call_command('web_scraper')
        
        self.stdout.write('Starting data import process...')
        call_command('data_import')
        
        self.stdout.write(self.style.SUCCESS('Successfully updated quotes'))