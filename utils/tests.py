# from django.core.management import call_command
# from django.test import TestCase
# from unittest.mock import patch
#
# from library.models.author import Author
# from library.models.book import Book
# from library.models.genre import Genre
#
#
# class ImportBooksCommandTestCase(TestCase):
#     @patch('requests.get')
#     def test_import_books_success(self, mock_get):
#         # Mock the API response
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.json.return_value = {
#             'items': [
#                 {
#                     'volumeInfo': {
#                         'title': 'Test Book',
#                         'description': 'Test Description',
#                         'publishedDate': '2022-01-01',
#                         'authors': ['Test Author'],
#                         'categories': ['Test Genre']
#                     }
#                 }
#             ]
#         }
#
#         # Call the custom command
#         call_command('import_books')
#
#         # Assert that the book and author were created
#         self.assertTrue(Author.objects.filter(first_name='Test', last_name='Author').exists())
#         self.assertTrue(Book.objects.filter(title='Test Book').exists())
#         self.assertTrue(Genre.objects.filter(genre_name='Test Genre').exists())
#
#     @patch('requests.get')
#     def test_import_books_failure(self, mock_get):
#         # Mock the API response to simulate failure
#         mock_get.return_value.status_code = 404
#
#         # Call the custom command
#         with self.assertRaises(SystemExit):
#             call_command('import_books')
from library.models.author import Author
from library.models.book import Book
from library.models.genre import Genre

Book.objects.all().delete()
Author.objects.all().delete()
Genre.objects.all().delete()
