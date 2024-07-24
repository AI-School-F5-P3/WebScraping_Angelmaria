# quotes/views.py

from django.shortcuts import render, get_object_or_404
from .models import Quote, Author

def quote_list(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/quote_list.html', {'quotes': quotes})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})
