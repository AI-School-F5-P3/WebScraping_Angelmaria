# Importamos las librerías necesarias
from django.core.management.base import BaseCommand  # Para crear un comando de Django
import requests  # Para hacer peticiones HTTP
from bs4 import BeautifulSoup  # Para analizar HTML
import json  # Para manejar datos JSON
import re  # Para usar expresiones regulares

# Definimos nuestro comando como una clase que hereda de BaseCommand
class Command(BaseCommand):
    help = 'Scrapes quotes from the website and saves them to a JSON file'

    # Método para limpiar el texto
    def clean_text(self, text):
        # Reemplaza múltiples espacios en blanco por uno solo
        text = re.sub(r'\s+', ' ', text).strip()
        # Elimina caracteres especiales, manteniendo puntuación básica
        text = re.sub(r'[^\w\s.,!?;:"-]', '', text)
        return text

    # Método principal que se ejecuta cuando se llama al comando
    def handle(self, *args, **options):
        base_url = "https://quotes.toscrape.com"
        quotes = []  # Lista para almacenar todas las citas
        authors = {}  # Diccionario para almacenar información de los autores
        page = 1  # Contador de páginas

        # Bucle para recorrer todas las páginas
        while True:
            url = f"{base_url}/page/{page}/"
            response = requests.get(url)
            if response.status_code != 200:
                break  # Si la página no existe, salimos del bucle
            
            soup = BeautifulSoup(response.content, 'html.parser')
            quotes_divs = soup.find_all('div', class_='quote')
            
            if not quotes_divs:
                break  # Si no hay citas en la página, salimos del bucle
            
            # Recorremos cada cita en la página
            for quote_div in quotes_divs:
                quote = {
                    'text': self.clean_text(quote_div.find('span', class_='text').text.strip('"')),
                    'author': self.clean_text(quote_div.find('small', class_='author').text),
                    'tags': [self.clean_text(tag.text) for tag in quote_div.find_all('a', class_='tag')]
                }
                quotes.append(quote)
                
                # Si es un autor nuevo, obtenemos su información
                if quote['author'] not in authors:
                    author_url = base_url + quote_div.find('a')['href']
                    self.scrape_author_about(author_url, quote['author'], authors)
            
            page += 1  # Pasamos a la siguiente página

        # Preparamos los datos para guardar en JSON
        data = {
            'quotes': quotes,
            'authors': authors
        }

        # Guardamos los datos en un archivo JSON
        with open('quotes_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Imprimimos un mensaje de éxito
        self.stdout.write(self.style.SUCCESS(f'Successfully scraped {len(quotes)} quotes and saved to quotes_data.json'))

# Método para obtener la información de un autor
    def scrape_author_about(self, author_url, author_name, authors):
        # Hacemos una petición GET a la página del autor
        response = requests.get(author_url)
        if response.status_code == 200:
            # Si la petición es exitosa, parseamos el contenido HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            # Encontramos la descripción del autor y la limpiamos
            about = self.clean_text(soup.find('div', class_='author-description').text)
            # Añadimos la información del autor al diccionario de autores
            authors[author_name] = about