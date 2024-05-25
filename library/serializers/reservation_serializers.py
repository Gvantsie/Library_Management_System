from rest_framework import serializers

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