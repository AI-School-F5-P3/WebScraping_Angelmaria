import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xyz_quotes.settings")
django.setup()

from quotes.models import Author, Quote

def import_data():
    with open('quotes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        author, created = Author.objects.get_or_create(
            name=item['author'],
            defaults={'about': item.get('author_about', '')}
        )
        
        Quote.objects.create(
            text=item['text'],
            author=author,
            tags=item['tags']
        )

    print(f"Imported {len(data)} quotes to the database.")

if __name__ == "__main__":
    import_data()