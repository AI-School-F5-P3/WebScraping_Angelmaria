# quotes/management/commands/update_quotes.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
import schedule
import time
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Runs web scraping and data import at regular intervals'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting quote update scheduler'))
        self.schedule_jobs()
        while True:
            schedule.run_pending()
            time.sleep(1)

    def schedule_jobs(self):
        # Schedule the job to run daily at midnight
        schedule.every().day.at("00:00").do(self.run_update)

    def run_update(self):
        try:
            self.stdout.write(self.style.SUCCESS('Starting web scraping...'))
            call_command('web_scraper')
            
            self.stdout.write(self.style.SUCCESS('Web scraping completed. Starting data import...'))
            call_command('data_import')
            
            self.stdout.write(self.style.SUCCESS('Quote update completed successfully'))
        except Exception as e:
            logger.error(f"An error occurred during quote update: {str(e)}")
            self.stdout.write(self.style.ERROR(f'Quote update failed: {str(e)}'))

if __name__ == '__main__':
    command = Command()
    command.handle()