from rest_framework import serializers

from library.models.book import Book


# Create your serializers here
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookStatisticsSerializer(serializers.ModelSerializer):
    last_year_loans = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ['title', 'author', 'times_borrowed', 'last_year_loans']
        