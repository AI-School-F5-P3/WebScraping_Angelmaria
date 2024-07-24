# quotes/views.py

from django.shortcuts import render, get_object_or_404
from .models import Quote, Author

def quote_list(request):
    # Obtener todas las citas
    quotes = Quote.objects.all()
    
    # Obtener todos los autores para el filtro
    authors = Author.objects.all()
    
    # Filtrar citas por autor si se ha seleccionado uno
    selected_author_id = request.GET.get('author')
    if selected_author_id:
        quotes = quotes.filter(author_id=selected_author_id)
    
    return render(request, 'quotes/quote_list.html', {'quotes': quotes, 'authors': authors})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})
