from django.contrib import admin

from library.models.author import Author
from library.models.book import Book
from library.models.genre import Genre
from library.models.transaction import BookTransaction


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'stock', 'times_borrowed', 'total_copies',)
    list_filter = ('title', 'author', 'status', 'genre',)
    search_fields = ('title', 'author', 'status', 'genre',)
    list_per_page = 20


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    list_filter = ('first_name', 'last_name',)
    search_fields = ('first_name', 'last_name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_filter = ('genre_name',)
    search_fields = ('genre_name',)
    list_display = ('genre_name',)


@admin.register(BookTransaction)
class BookTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_at', 'returned_at')

