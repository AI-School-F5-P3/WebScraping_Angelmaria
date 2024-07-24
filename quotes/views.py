# quotes/views.py
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Quote, Author

def quote_list(request):
    author_id = request.GET.get('author')
    quotes = Quote.objects.all()

    # Filtrar por autor si se ha seleccionado uno
    if author_id:
        quotes = quotes.filter(author_id=author_id)

    # Paginación
    paginator = Paginator(quotes, 10)  # Muestra 10 citas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Obtener la lista de autores para el formulario
    authors = Author.objects.all()

    return render(request, 'quotes/quote_list.html', {
        'page_obj': page_obj,
        'authors': authors,
        'selected_author': author_id
    })

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})
