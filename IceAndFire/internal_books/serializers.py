from rest_framework import serializers

from internal_books.models import Book


# Bool Serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

