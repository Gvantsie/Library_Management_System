from django.urls import path

from library.views.reservation import BookListView, ReserveBookView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('reserve/<int:book_id>/', ReserveBookView.as_view(), name='reserve-book'),

]
