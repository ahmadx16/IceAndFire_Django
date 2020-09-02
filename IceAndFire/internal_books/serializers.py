from rest_framework import serializers

from internal_books.models import Book, Author
from .models import update_authors, new_book_authors


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']

    def to_representation(self, instance):
        author = super().to_representation(instance)
        return author['name']

    def to_internal_value(self, data):
        return super().to_internal_value({"name": data})


class BookSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'isbn', 'authors', 'number_of_pages', 'publisher', 'country', 'release_date']


    def create(self, validated_data):
        authors = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        new_authors = [author['name'] for author in authors]
        # add new authors to book
        new_book_authors(book, new_authors)
        
        return book

    def update(self, book, validated_data):
        authors = validated_data.pop('authors', None)
        # updating authors if given in request
        update_authors(authors, book)
        # updating to new values from request
        for (key, value) in validated_data.items():
            setattr(book, key, value)
        book.save()

        return book

    
    
