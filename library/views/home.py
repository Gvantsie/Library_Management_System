from django.shortcuts import render

from library.models.book import Book


def home(request):
    # Query the most borrowed books
    most_borrowed_books = Book.objects.order_by('-times_borrowed')[:3]
    return render(request, 'home.html', {'most_borrowed_books': most_borrowed_books})
