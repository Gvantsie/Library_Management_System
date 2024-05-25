from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q

from TBC_final import settings
from library.models.book import Book
from library.serializers.book_serializers import BookSerializer, BookStatisticsSerializer
from users.models import CustomUser


class PopularBooksAPIView(APIView):
    def get(self, request):
        popular_books = Book.objects.annotate(
            loan_count=Count('reservations', filter=Q(reservations__status='reserved'))
        ).order_by('-times_borrowed')[:10]
        serializer = BookSerializer(popular_books, many=True)
        return Response(serializer.data)


class BookStatisticsAPIView(APIView):
    def get(self, request):
        one_year_ago = timezone.now() - timezone.timedelta(days=365)

        book_stats = Book.objects.annotate(
            loan_count=Count('reservations', filter=Q(reservations__status='reserved')),
            last_year_loans=Count('reservations', filter=Q(reservations__status='reserved',
                                                           reservations__reserved_at__gte=one_year_ago))
        ).order_by('-times_borrowed')

        serializer = BookStatisticsSerializer(book_stats, many=True)
        return Response(serializer.data)


class LateReturnedBooksAPIView(APIView):
    def get(self, request):
        late_returned_books = Book.objects.annotate(
            late_returns=Count('reservations', filter=Q(reservations__is_late=True))
        ).order_by('-late_returns')[:100]

        serialized_data = []
        for book in late_returned_books:
            late_reservations = book.reservations.filter(is_late=True)
            serialized_data.append({
                'title': book.title,
                'author': book.author.name,
                'late_returns': book.late_returns,
                'late_reservations': [
                    {
                        'user': reservation.user.email,
                        'due_date': reservation.due_date,
                        'return_date': reservation.return_date,
                    }
                    for reservation in late_reservations
                ]
            })

        return Response(serialized_data)


class LateReturnedUsersAPIView(APIView):
    def get(self, request):
        late_returned_users = settings.AUTH_USER_MODEL.objects.annotate(
            late_returns=Count('reservations', filter=Q(reservations__is_late=True))
        ).order_by('-late_returns')[:100]

        serialized_data = []
        for user in late_returned_users:
            late_reservations = user.reservations.filter(is_late=True)
            serialized_data.append({
                'user': user.email,
                'personal_number': user.personal_number,
                'birth_date': user.birth_date,
                'late_returns': user.late_returns,
                'late_reservations': [
                    {
                        'book': reservation.book.title,
                        'due_date': reservation.due_date,
                        'return_date': reservation.return_date,
                    }
                    for reservation in late_reservations
                ]
            })

        return Response(serialized_data)
