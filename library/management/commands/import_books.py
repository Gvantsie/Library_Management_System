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
# from django.core.management.base import BaseCommand
# from library.factories import BookFactory, GenreFactory, AuthorFactory, fake
# from library.models.book import Book
# import random
# import threading
#
# class ImportBooksThread(threading.Thread):
#     def __init__(self, books, genres):
#         super().__init__()
#         self.books = books
#         self.genres = genres
#
#     def run(self):
#         for book in self.books:
#             selected_genres = random.sample(self.genres, min(3, len(self.genres)))  # Restrict to max 3 genres
#             for genre in selected_genres:
#                 book.genre.add(genre)
#
#
# class Command(BaseCommand):
#     help = 'Import 1000 books with associated genres'
#
#     def handle(self, *args, **options):
#         num_books = 1000
#         num_genres = 5
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
#         # Split the books into chunks
#         chunk_size = num_books // num_genres
#         book_chunks = [books[i:i+chunk_size] for i in range(0, num_books, chunk_size)]
#
#         # Create and start threads for each chunk
#         threads = []
#         for chunk in book_chunks:
#             thread = ImportBooksThread(chunk, genres)
#             thread.start()
#             threads.append(thread)
#
#         # Wait for all threads to finish
#         for thread in threads:
#             thread.join()


import threading
from django.core.management import BaseCommand
from library.models.genre import Genre


class Command(BaseCommand):
    help = 'Imports books into the database(Command <num_books> <num_threads>).'

    def add_arguments(self, parser):
        parser.add_argument('num_books', type=int, help='Number of books to import')
        parser.add_argument('num_threads', type=int, help='Number of threads to use')

    def handle(self, *args, **options):
        num_books = options['num_books']
        num_threads = options['num_threads']

        # Calculate the number of books per thread
        books_per_thread = num_books // num_threads

        threads = []
        for i in range(num_threads):
            if i == num_threads - 1:
                # The last thread will handle the remaining books
                num_books_for_thread = num_books - (books_per_thread * i)
            else:
                num_books_for_thread = books_per_thread

            thread = threading.Thread(target=self.import_books_with_genres, args=(num_books_for_thread,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {num_books} books.'))

    def import_books_with_genres(self, num_books):
        genres_list = ['Fantasy', 'Science Fiction', 'Mystery', 'Romance', 'Thriller', 'Horror', 'Historical Fiction',
                       'Non-fiction', 'Biography', 'Self-help']

        for genre_name in genres_list:
            # Create or get Genre object using genre_name
            genre, created = Genre.objects.get_or_create(genre_name=genre_name)
