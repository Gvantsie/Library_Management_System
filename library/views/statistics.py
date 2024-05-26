from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q, F

from library.models.book import Book
from library.models.reservation import Reservation
from library.serializers.book_serializers import BookSerializer, BookStatisticsSerializer
from library.views.book import MyPagination
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

        paginator = MyPagination()
        result_page = paginator.paginate_queryset(book_stats, request)
        serializer = BookStatisticsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class LateReturnedBooksAPIView(APIView):
    def get(self, request):
        # Get the current date
        current_date = timezone.now().date()

        # Filter late returned reservations
        late_reservations = Reservation.objects.filter(return_date__gt=F('due_date'))

        # Aggregate late returned reservations per book
        late_returned_books = Book.objects.annotate(
            late_returns=Count('reservations', filter=Q(reservations__in=late_reservations))
        ).order_by('-late_returns')[:100]

        serialized_data = []
        for book in late_returned_books:
            late_reservations = late_reservations.filter(book=book)
            serialized_data.append({
                'title': book.title,
                'author': book.author.first_name + ' ' + book.author.last_name,
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
        # Get the current date
        current_date = timezone.now().date()

        # Filter late returned reservations
        late_reservations = Reservation.objects.filter(return_date__gt=F('due_date'))

        # Annotate users with the count of their late returns
        late_returned_users = CustomUser.objects.annotate(
            late_returns=Count('reservations', filter=Q(reservations__in=late_reservations))
        ).order_by('-late_returns')[:100]

        serialized_data = []
        for user in late_returned_users:
            # Filter late reservations for this user
            user_late_reservations = late_reservations.filter(user=user)

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
                    for reservation in user_late_reservations
                ]
            })

        return Response(serialized_data)
