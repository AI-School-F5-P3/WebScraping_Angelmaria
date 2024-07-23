# Web Scraping con Django

## Descripción
Este proyecto utiliza Django para hacer scraping de frases desde [quotes.toscrape.com](https://quotes.toscrape.com) y almacenarlas en MySQL.

## Tecnologías Utilizadas
- Django
- Requests
- BeautifulSoup
- MySQL

## Instrucciones
1. Clona el repositorio.
2. Configura un entorno virtual y las dependencias.
3. Configura la base de datos MySQL.
4. Ejecuta `python manage.py migrate`.
5. Ejecuta `python manage.py scrape_quotes`.
6. Ejecuta el servidor Django con `python manage.py runserver`.

## Estructura del Proyecto
- `quotes_project/`: Configuración principal del proyecto.
- `quotes/`: Aplicación Django que maneja el scraping y la visualización de datos.
