from rest_framework import serializers

from internal_books.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret['name']


class BookSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('name', 'isbn', 'authors', 'number_of_pages', 'publisher', 'country', 'release_date')
