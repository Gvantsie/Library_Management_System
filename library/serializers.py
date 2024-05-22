# serializers.py
from rest_framework import serializers

from library.models.book import Book
from library.models.reservation import Reservation


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # to use only authenticated users

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'book', 'reserved_at', 'status']
        read_only_fields = ['reserved_at', 'status']
