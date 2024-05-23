import concurrent.futures
import random
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from utils.factories import create_authors, BookFactory, GENRE_CHOICES
from library.models.genre import Genre


class Command(BaseCommand):
    help = 'Import books into the database using concurrent features'

    def add_arguments(self, parser):
        parser.add_argument('num_books', type=int, help='Number of books to import')

    def handle(self, *args, **options):
        num_books = options['num_books']
        num_authors = num_books // 5  # Example ratio of authors to books

        self.stdout.write(self.style.NOTICE('Creating authors...'))
        authors = create_authors(num_authors)

        def create_book(_):
            author = random.choice(authors)
            book = BookFactory(author=author)
            genres = random.choices(GENRE_CHOICES, k=random.randint(1, 3))
            book.save()

            for genre_name in genres:
                self.add_genre_to_book(book, genre_name)

            return book

        self.stdout.write(self.style.NOTICE('Creating books...'))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(create_book, i) for i in range(num_books)]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating book: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {num_books} books.'))

    def add_genre_to_book(self, book, genre_name):
        with transaction.atomic():
            genre, created = Genre.objects.select_for_update().get_or_create(genre_name=genre_name)
            book.genre.add(genre)  # Use 'genre' instead of 'genres'
