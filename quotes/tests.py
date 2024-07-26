# quotes/tests.py
import json
from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

class WebScraperTests(TestCase):
    
    @patch('requests.get')
    def test_scrape_quotes_success(self, mock_get):
        # Simular una respuesta HTTP exitosa con BeautifulSoup
        html_content = '''
        <html>
            <body>
                <div class="quote">
                    <span class="text">"Life is what happens when you're busy making other plans."</span>
                    <small class="author">John Lennon</small>
                    <div class="tags">
                        <a class="tag">life</a>
                        <a class="tag">plans</a>
                    </div>
                    <a href="/author/John-Lennon">Author Page</a>
                </div>
            </body>
        </html>
        '''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = html_content
        mock_get.return_value = mock_response

        # Llamar al comando de gestión para ejecutar el scraper
        call_command('web_scraper')

        # Verificar que el archivo JSON se haya creado correctamente
        with open('quotes_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data['quotes']), 1)
            self.assertEqual(data['quotes'][0]['text'], "Life is what happens when you're busy making other plans.")
            self.assertEqual(data['quotes'][0]['author'], "John Lennon")
            self.assertListEqual(data['quotes'][0]['tags'], ["life", "plans"])

    @patch('requests.get')
    def test_scrape_author_info_success(self, mock_get):
        # Simular una respuesta HTTP exitosa con BeautifulSoup
        html_content = '''
        <html>
            <body>
                <span class="author-born-date">October 9, 1940</span>
                <span class="author-born-location">in Liverpool, England</span>
                <div class="author-description">John Lennon was an English singer, songwriter, and peace activist.</div>
            </body>
        </html>
        '''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = html_content
        mock_get.return_value = mock_response

        # Crear una instancia de la clase Command para probar scrape_author_info
        from quotes.management.commands.web_scraper import Command
        cmd = Command()
        author_info = cmd.scrape_author_info("https://quotes.toscrape.com/author/John-Lennon/")

        # Verificar que la información del autor se haya extraído correctamente
        self.assertEqual(author_info['born'], '1940-10-09')
        self.assertEqual(author_info['birth_place'], 'Liverpool, England')
        self.assertEqual(author_info['about'], 'John Lennon was an English singer, songwriter, and peace activist.')

    @patch('requests.get')
    def test_convert_date(self, mock_get):
        # Crear una instancia de la clase Command para probar convert_date
        from quotes.management.commands.web_scraper import Command
        cmd = Command()

        # Probar la conversión de fechas
        self.assertEqual(cmd.convert_date('October 9, 1940'), '1940-10-09')
        self.assertIsNone(cmd.convert_date('Invalid Date'))

    @patch('requests.get')
    def test_scrape_quotes_no_quotes(self, mock_get):
        # Simular una respuesta HTTP sin citas
        html_content = '''
        <html>
            <body>
                <div class="no-quotes"></div>
            </body>
        </html>
        '''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = html_content
        mock_get.return_value = mock_response

        # Llamar al comando de gestión para ejecutar el scraper
        call_command('web_scraper')

        # Verificar que el archivo JSON se haya creado correctamente pero sin citas
        with open('quotes_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data['quotes']), 0)
