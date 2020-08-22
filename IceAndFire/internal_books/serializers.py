from rest_framework import serializers

from internal_books.models import Book


# Bool Serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        """Convert  to lowercase."""
        raw_obj = super().to_representation(instance)

        return raw_obj
