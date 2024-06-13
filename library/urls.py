from django.urls import path

from library.views.book import BookListView, BookDetailView
from library.views.reservation import (ReserveBookView,
                                       ReturnBookView,
                                       MarkBookReturnedView)
from library.views.statistics import (PopularBooksAPIView,
                                      BookStatisticsAPIView,
                                      LateReturnedBooksAPIView,
                                      LateReturnedUsersAPIView)


urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('reservations/<int:reservation_id>/return/', ReturnBookView.as_view(), name='return-book'),
    path('reservations/<int:pk>/mark-returned/', MarkBookReturnedView.as_view(), name='mark-book-returned'),
    path('statistics/popular-books/', PopularBooksAPIView.as_view(), name='popular-books'),
    path('statistics/book-stats/', BookStatisticsAPIView.as_view(), name='book-stats'),
    path('statistics/late-returned-books/', LateReturnedBooksAPIView.as_view(), name='late-returned-books'),
    path('statistics/late-returned-users/', LateReturnedUsersAPIView.as_view(), name='late-returned-users'),
]
