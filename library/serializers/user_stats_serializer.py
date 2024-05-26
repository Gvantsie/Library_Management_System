from rest_framework.serializers import ModelSerializer

from library.models.user_stats import UserStatistics


class UserStatisticsSerializer(ModelSerializer):
    class Meta:
        model = UserStatistics
        fields = ['books_read', 'books_reserved']
