import requests
from bs4 import BeautifulSoup
import json
import re

class QuoteScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.quotes = []
        self.authors = {}

    def clean_text(self, text):
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters except punctuation
        text = re.sub(r'[^\w\s.,!?;:"-]', '', text)
        return text

    def scrape_quotes(self):
        page = 1
        while True:
            url = f"{self.base_url}/page/{page}/"
            response = requests.get(url)
            if response.status_code != 200:
                break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            quotes_divs = soup.find_all('div', class_='quote')
            
            if not quotes_divs:
                break
            
            for quote_div in quotes_divs:
                quote = {
                    'text': self.clean_text(quote_div.find('span', class_='text').text.strip('"')),
                    'author': self.clean_text(quote_div.find('small', class_='author').text),
                    'tags': [self.clean_text(tag.text) for tag in quote_div.find_all('a', class_='tag')]
                }
                self.quotes.append(quote)
                
                if quote['author'] not in self.authors:
                    author_url = self.base_url + quote_div.find('a')['href']
                    self.scrape_author_about(author_url, quote['author'])
            
            page += 1

    def scrape_author_about(self, author_url, author_name):
        response = requests.get(author_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            about = self.clean_text(soup.find('div', class_='author-description').text)
            self.authors[author_name] = about

    def save_to_json(self, filename):
        data = {
            'quotes': self.quotes,
            'authors': self.authors
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scraper = QuoteScraper("https://quotes.toscrape.com")
    scraper.scrape_quotes()
    scraper.save_to_json("quotes_data.json")
    print(f"Scraped {len(scraper.quotes)} quotes and {len(scraper.authors)} authors. Data saved to quotes_data.json")