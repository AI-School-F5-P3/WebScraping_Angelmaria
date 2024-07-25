# your_app/management/commands/number_quotes_author.py

from django.core.management.base import BaseCommand
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from quotes.models import Quote, Author

class Command(BaseCommand):
    help = 'Prints the number of quotes by each author and displays a bar chart'

    def handle(self, *args, **kwargs):
        # Obtener datos de citas
        quotes = Quote.objects.all().values('author_id')
        authors = Author.objects.all().values('id', 'name')

        # Convertir a DataFrames
        quotes_df = pd.DataFrame(list(quotes))
        authors_df = pd.DataFrame(list(authors))

        # Contar citas por autor
        quotes_by_author = quotes_df.groupby('author_id').size().reset_index(name='quote_count')
        authors_with_quote_count = authors_df.merge(quotes_by_author, left_on='id', right_on='author_id')

        # Mostrar el resultado en consola
        print(authors_with_quote_count)

        # Crear gráfica de barras
        plt.figure(figsize=(10, 8))
        sns.barplot(x='quote_count', y='name', data=authors_with_quote_count.sort_values('quote_count', ascending=False))
        plt.title('Number of Quotes by Author')
        plt.xlabel('Number of Quotes')
        plt.ylabel('Author')
        plt.tight_layout()

        # Mostrar la gráfica
        plt.show()
