from django.shortcuts import render
from search_engine import search_database


def search_form(request):
    return render(request, 'search/search_form.html')

def search_results(request):
    if request.method == 'POST':
        query = request.POST.get('keywords', '')
        matches = search_database.search(query)
        print(query)
        return render(request, 'search/search_results.html', {'query': query, 'matching_books': matches})
    
    return render(request, 'search/search_form.html')