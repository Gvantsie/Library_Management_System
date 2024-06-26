from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from library.models.book import Book
from library.models.reservation import Reservation
from library.serializers.reservation_serializers import ReservationSerializer, ReservationReturnSerializer


# Create your views here
# Endpoint to reserve a book
class ReserveBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if book.stock > 0:
            try:
                reservation = Reservation.objects.create(user=request.user, book=book)
                book.stock -= 1
                book.save()
                serializer = ReservationSerializer(reservation)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
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
            reservation.returned = True
            reservation.return_date = timezone.now().date()
            reservation.book.copies_available += 1
            reservation.book.save()
            reservation.save(update_fields=['status', 'returned', 'return_date'])
            return Response(status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response({"detail": "Invalid reservation ID or reservation already returned."}, status=status.HTTP_400_BAD_REQUEST)


# Endpoint to mark a book as returned
class MarkBookReturnedView(generics.UpdateAPIView):
    queryset = Reservation.objects.filter(returned=False)
    serializer_class = ReservationReturnSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(returned=True)
        return Response(serializer.data)