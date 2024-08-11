from django.test import TestCase, Client
from django.urls import reverse

class SearchViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_search_form_view(self):
        """Test the search form view"""
        response = self.client.get(reverse('evidence_book_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search_form.html')

    def test_search_results_view_post(self):
        """Test the search results view with a POST request"""
        response = self.client.post(reverse('search_results'), {'keywords': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search_results.html')
        self.assertIn('query', response.context)
        self.assertIn('matching_books', response.context)

    def test_search_results_view_get(self):
        """Test that a GET request to search results redirects to the search form"""
        response = self.client.get(reverse('search_results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search_form.html')