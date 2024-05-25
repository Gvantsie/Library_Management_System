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
    date_of_death = factory.LazyFunction(lambda: fake.date_this_decade(before_today=True))


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    author = factory.SubFactory(AuthorFactory)
    title = factory.Faker('sentence', nb_words=6)
    description = factory.Faker('text', max_nb_chars=200)
    stock = factory.Faker('random_int', min=1, max=100)
    publication_date = factory.Faker('date_this_decade', before_today=True)
    cover_type = factory.Iterator(['hard', 'soft'])
    status = 'available'

    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of genres were passed in, use them
            for genre in extracted:
                self.genres.add(genre)
