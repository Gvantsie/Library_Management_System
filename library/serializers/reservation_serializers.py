from rest_framework import serializers

from library.models.book import Book
from library.models.reservation import Reservation


# Create your serializers here
class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # to use only authenticated users

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'book', 'reserved_at', 'status']
        read_only_fields = ['reserved_at', 'status']


class ReservationReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['returned']
        read_only_fields = ['user', 'book', 'reserved_at']


class LateReturnedBookSerializer(serializers.ModelSerializer):
    late_returns = serializers.IntegerField()
    late_reservations = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['title', 'author', 'late_returns', 'late_reservations']

    def get_late_reservations(self, obj):
        late_reservations = Reservation.objects.filter(
            book=obj, return_date__gt=F('due_date')
        )
        return [
            {
                'user': reservation.user.email,
                'due_date': reservation.due_date,
                'return_date': reservation.return_date,
            }
            for reservation in late_reservations
        ]
