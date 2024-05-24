from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from library.models.book import Book
from library.models.reservation import Reservation
from library.serializers import BookSerializer, ReservationSerializer


# Create your views here
# Endpoint to reserve a book
class ReserveBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        book = Book.objects.get(id=book_id)
        if book.copies_available > 0:
            try:
                reservation = Reservation.objects.create(user=request.user, book=book)
                book.copies_available -= 1
                book.save()
                serializer = ReservationSerializer(reservation)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "This book is not available for reservation."}, status=status.HTTP_400_BAD_REQUEST)


# Endpoint to cancel the reservation
class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id, user=request.user, status='reserved')
            reservation.status = 'returned'
            reservation.book.copies_available += 1
            reservation.book.save()
            reservation.save()
            return Response(status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response({"detail": "Invalid reservation ID or reservation already returned."}, status=status.HTTP_400_BAD_REQUEST)