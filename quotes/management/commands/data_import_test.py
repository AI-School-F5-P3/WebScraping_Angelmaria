# Este es un comando de Django ubicado en la carpeta management/commands de la app quotes
# quotes/management/commands/data_import.py

# Importamos las clases y módulos necesarios
from django.core.management.base import BaseCommand  # Para crear un comando de Django
from quotes.models import Author, Quote, Tag  # Importamos los modelos de nuestra app
import json  # Para manejar datos JSON

# Definimos nuestro comando como una clase que hereda de BaseCommand
class Command(BaseCommand):
    # Descripción del comando que se mostrará al usar python manage.py help
    help = 'Imports quotes data from JSON file to the database'

    # Método principal que se ejecuta cuando se llama al comando
    def handle(self, *args, **options):
        # Abrimos el archivo JSON en modo lectura
        with open('quotes_data.json', 'r', encoding='utf-8') as f:
            # Cargamos los datos JSON en un diccionario de Python
            data = json.load(f)

        # Importamos los autores
        for author_name, about in data['authors'].items():
            # Creamos o actualizamos cada autor en la base de datos
            Author.objects.get_or_create(name=author_name, defaults={'about': about})

        # Importamos las citas y etiquetas
        for quote_data in data['quotes']:
            # Obtenemos el autor de la cita (que ya debe existir en la base de datos)
            author = Author.objects.get(name=quote_data['author'])
            # Creamos la cita en la base de datos
            quote = Quote.objects.create(text=quote_data['text'], author=author)

            # Procesamos las etiquetas de la cita
            for tag_name in quote_data['tags']:
                # Creamos o obtenemos la etiqueta
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                # Asociamos la etiqueta a la cita
                quote.tags.add(tag)

        # Imprimimos un mensaje de éxito con el número de citas y autores importados
        self.stdout.write(self.style.SUCCESS(f"Imported {len(data['quotes'])} quotes and {len(data['authors'])} authors to the database."))