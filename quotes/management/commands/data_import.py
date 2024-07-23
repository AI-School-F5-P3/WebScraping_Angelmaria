import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xyz_quotes.settings")
django.setup()

from quotes.models import Author, Quote, Tag

def import_data():
    with open('quotes_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Import authors
    for author_name, about in data['authors'].items():
        Author.objects.get_or_create(name=author_name, defaults={'about': about})

    # Import quotes and tags
    for quote_data in data['quotes']:
        author = Author.objects.get(name=quote_data['author'])
        quote = Quote.objects.create(text=quote_data['text'], author=author)

        for tag_name in quote_data['tags']:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)

    print(f"Imported {len(data['quotes'])} quotes and {len(data['authors'])} authors to the database.")

if __name__ == "__main__":
    import_data()