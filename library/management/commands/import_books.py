import threading

from django.core.management import BaseCommand

from utils.factories import import_books


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

            thread = threading.Thread(target=import_books, args=(num_books_for_thread,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {num_books} books.'))
