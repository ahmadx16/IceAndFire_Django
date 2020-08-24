from rest_framework import serializers

from internal_books.models import Book, BookAndAuthors


class BookAndAuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAndAuthors
        fields = ('author',)


class BookSerializer(serializers.ModelSerializer):

    authors = BookAndAuthorsSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('name', 'isbn', 'authors', 'number_of_pages', 'publisher', 'country', 'release_date')
