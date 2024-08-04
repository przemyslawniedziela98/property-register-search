from django.shortcuts import render


def search_form(request):
    return render(request, 'search/search_form.html')

def search_results(request):
    if request.method == 'POST':
        #TBD
        return render(request, 'search/search_results.html', {'query': None, 'matching_books': None})
    
    return render(request, 'search/search_form.html')