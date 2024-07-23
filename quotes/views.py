from django.shortcuts import render
from .models import Quote, Author

def quote_list(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/quote_list.html', {'quotes': quotes})

def author_detail(request, author_id):
    author = Author.objects.get(id=author_id)
    quotes = author.quote_set.all()
    return render(request, 'quotes/author_detail.html', {'author': author, 'quotes': quotes})