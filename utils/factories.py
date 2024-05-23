import factory
from faker import Faker
from django.utils import timezone
from library.models.author import Author
from library.models.book import Book
from library.models.genre import Genre


fake = Faker()


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    date_of_birth = factory.Faker('date_of_birth', tzinfo=timezone.get_current_timezone())
    date_of_death = factory.LazyAttribute(lambda obj: fake.date_between(start_date=obj.date_of_birth, end_date='+90y')
                                            if fake.boolean(chance_of_getting_true=30) else None)


def create_authors(num_authors):
    return AuthorFactory.create_batch(num_authors)


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('catch_phrase')
    description = factory.Faker('text')
    stock = factory.Faker('random_int', min=1, max=100)
    publication_date = factory.Faker('date')
    cover_type = factory.Faker('random_element', elements=['hard', 'soft'])
    status = 'available'
    author = factory.SubFactory(AuthorFactory)


GENRE_CHOICES = [
    'Fantasy', 'Science Fiction', 'Mystery', 'Thriller', 'Romance',
    'Historical Fiction', 'Horror', 'Biography', 'Self-Help', 'Travel',
    'Cooking', 'Art', 'Poetry', 'Drama'
]


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    genre_name = factory.Faker('random_element', elements=GENRE_CHOICES)
