import concurrent.futures
from django.core.management.base import BaseCommand
from utils.factories import create_authors, BookFactory, GenreFactory
from library.models.genre import Genre
import random

from utils.factories import GENRE_CHOICES


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
                genre, created = Genre.objects.get_or_create(genre_name=genre_name)
                book.genres.add(genre)
            return book

        self.stdout.write(self.style.NOTICE('Creating books...'))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(create_book, i) for i in range(num_books)]
            for future in concurrent.futures.as_completed(futures):
                future.result()

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {num_books} books.'))
