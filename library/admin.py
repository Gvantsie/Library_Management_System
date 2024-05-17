from django.contrib import admin

from library.models.author import Author
from library.models.book import Book
from library.models.genre import Genre


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'stock',)
    list_filter = ('title', 'author', 'status', 'genre',)
    search_fields = ('title', 'author', 'status', 'genre',)


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
