from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_form, name='evidence_book_search'), 
    path('results/', views.search_results, name='search_results')
]