# from django.core.management.base import BaseCommand
# from library.factories import BookFactory, GenreFactory, AuthorFactory, fake
# from library.models.book import Book
# import random
#
#
# class Command(BaseCommand):
#     help = 'Import 1000 books with associated genres'
#
#     def handle(self, *args, **options):
#         num_books = 1000
#         num_genres = 10
#
#         # Create genres
#         genres = GenreFactory.create_batch(num_genres)
#
#         # Bulk create books
#         books = []
#         for _ in range(num_books):
#             author = AuthorFactory()
#             title = fake.sentence(nb_words=6)
#             description = fake.text(max_nb_chars=200)
#             stock = fake.random_int(min=1, max=100)
#             publication_date = fake.date_this_decade(before_today=True)
#             cover_type = random.choice(['hard', 'soft'])
#             status = 'available'
#             book = Book.objects.create(author=author, title=title, description=description, stock=stock, publication_date=publication_date, cover_type=cover_type, status=status)
#             books.append(book)
#
#         # Assign genres to books
#         for book in books:
#             selected_genres = random.sample(genres, random.randint(1, num_genres))
#             for genre in selected_genres:
#                 book.genre.add(genre)
#
#         self.stdout.write(self.style.SUCCESS(f'Successfully imported {num_books} books.'))
#

# import books using threads to optimize performance
from django.core.management.base import BaseCommand
from library.factories import BookFactory, GenreFactory, AuthorFactory, fake
from library.models.book import Book
import random
import threading

class ImportBooksThread(threading.Thread):
    def __init__(self, books, genres):
        super().__init__()
        self.books = books
        self.genres = genres

    def run(self):
        for book in self.books:
            selected_genres = random.sample(self.genres, min(3, len(self.genres)))  # Restrict to max 3 genres
            for genre in selected_genres:
                book.genre.add(genre)


class Command(BaseCommand):
    help = 'Import 1000 books with associated genres'

    def handle(self, *args, **options):
        num_books = 1000
        num_genres = 5

        # Create genres
        genres = GenreFactory.create_batch(num_genres)

        # Bulk create books
        books = []
        for _ in range(num_books):
            author = AuthorFactory()
            title = fake.sentence(nb_words=6)
            description = fake.text(max_nb_chars=200)
            stock = fake.random_int(min=1, max=100)
            publication_date = fake.date_this_decade(before_today=True)
            cover_type = random.choice(['hard', 'soft'])
            status = 'available'
            book = Book.objects.create(author=author, title=title, description=description, stock=stock, publication_date=publication_date, cover_type=cover_type, status=status)
            books.append(book)

        # Split the books into chunks
        chunk_size = num_books // num_genres
        book_chunks = [books[i:i+chunk_size] for i in range(0, num_books, chunk_size)]

        # Create and start threads for each chunk
        threads = []
        for chunk in book_chunks:
            thread = ImportBooksThread(chunk, genres)
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

