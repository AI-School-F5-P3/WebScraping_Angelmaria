import requests
from bs4 import BeautifulSoup
import json

class QuoteScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.quotes = []

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
                    'text': quote_div.find('span', class_='text').text.strip('"'),
                    'author': quote_div.find('small', class_='author').text,
                    'tags': [tag.text for tag in quote_div.find_all('a', class_='tag')]
                }
                self.quotes.append(quote)
                
                # Scrape author's about page
                author_url = self.base_url + quote_div.find('a')['href']
                self.scrape_author_about(author_url, quote['author'])
            
            page += 1

    def scrape_author_about(self, author_url, author_name):
        response = requests.get(author_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            about = soup.find('div', class_='author-description').text.strip()
            
            # Add or update author information
            author_exists = False
            for quote in self.quotes:
                if quote['author'] == author_name:
                    quote['author_about'] = about
                    author_exists = True
                    break
            
            if not author_exists:
                self.quotes.append({'author': author_name, 'author_about': about})

    def save_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scraper = QuoteScraper("https://quotes.toscrape.com")
    scraper.scrape_quotes()
    scraper.save_to_json("quotes.json")
    print(f"Scraped {len(scraper.quotes)} quotes and saved to quotes.json")