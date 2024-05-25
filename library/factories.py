import factory
from faker import Faker

from library.models.author import Author
from library.models.book import Book
from library.models.genre import Genre

fake = Faker()


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    genre_name = factory.Faker('word')


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18)
    date_of_death = factory.Iterator([fake.date_this_decade(before_today=True) for _ in range(50)])


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    author = factory.SubFactory(AuthorFactory)
    genre = factory.RelatedFactoryList(GenreFactory, size=lambda: fake.random_int(min=1, max=3))
    title = factory.Faker('sentence', nb_words=6)
    description = factory.Faker('text', max_nb_chars=200)
    stock = factory.Faker('random_int', min=1, max=100)
    publication_date = factory.Faker('date_this_decade', before_today=True)
    cover_type = factory.Iterator(['hard', 'soft'])
    status = 'available'


def import_books(num_books):
    books = BookFactory.create_batch(num_books)
