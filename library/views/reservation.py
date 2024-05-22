# views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from library.models.book import Book
from library.models.reservation import Reservation

from library.serializers import BookSerializer, ReservationSerializer


# Create your views here.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReserveBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        book = Book.objects.get(id=book_id)
        if book.is_available():
            reservation, created = Reservation.objects.get_or_create(user=request.user, book=book)
            if created:
                book.stock -= 1
                if book.stock == 0:
                    book.status = 'unavailable'
                book.save()
                serializer = ReservationSerializer(reservation)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "You have already reserved this book."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "This book is not available for reservation."}, status=status.HTTP_400_BAD_REQUEST)
