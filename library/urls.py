from django.urls import path

from library.views.book import BookListView, BookDetailView
from library.views.reservation import ReserveBookView, ReturnBookView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:book_id>/reserve/', ReserveBookView.as_view(), name='reserve-book'),
    path('reservations/<int:reservation_id>/return/', ReturnBookView.as_view(), name='return-book'),

]
