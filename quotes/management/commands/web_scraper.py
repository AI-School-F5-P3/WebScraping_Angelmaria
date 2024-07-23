# quotes/management/commands/web_scraper.py

from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Scrapes quotes and author information from the website'

    def handle(self, *args, **options):
        self.scrape_quotes()

    def scrape_quotes(self):
        base_url = "https://quotes.toscrape.com"
        quotes = []
        authors = {}
        page = 1

        while True:
            url = f"{base_url}/page/{page}/"
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.RequestException as e:
                self.stdout.write(self.style.WARNING(f"Failed to fetch page {page}: {str(e)}"))
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            quote_divs = soup.find_all('div', class_='quote')

            if not quote_divs:
                break

            for quote_div in quote_divs:
                quote = {
                    'text': quote_div.find('span', class_='text').text.strip('"'),
                    'author': quote_div.find('small', class_='author').text,
                    'tags': [tag.text for tag in quote_div.find_all('a', class_='tag')]
                }
                quotes.append(quote)

                if quote['author'] not in authors:
                    author_url = base_url + quote_div.find('a')['href']
                    author_info = self.scrape_author_info(author_url)
                    if author_info:
                        authors[quote['author']] = author_info

            page += 1

        data = {
            'quotes': quotes,
            'authors': authors
        }

        try:
            with open('quotes_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.stdout.write(self.style.SUCCESS(f'Successfully scraped {len(quotes)} quotes and {len(authors)} authors'))
        except IOError as e:
            self.stdout.write(self.style.ERROR(f"Failed to write data to file: {str(e)}"))

    def scrape_author_info(self, author_url):
        try:
            response = requests.get(author_url)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.WARNING(f"Failed to fetch author info from {author_url}: {str(e)}"))
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        
        born_date = soup.find('span', class_='author-born-date').text
        born_location = soup.find('span', class_='author-born-location').text
        about = soup.find('div', class_='author-description').text.strip()

        return {
            'born': born_date,
            'birth_place': born_location.strip('in '),
            'about': about
        }