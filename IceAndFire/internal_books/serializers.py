from rest_framework import serializers

from internal_books.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret['name']

    def to_internal_value(self, data):
        return super().to_internal_value({"name": data})


class BookSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True, read_only=False)

    class Meta:
        model = Book
        fields = ('name', 'isbn', 'authors', 'number_of_pages', 'publisher', 'country', 'release_date')

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        for author_data in authors_data:
            Author.objects.create(book=book, **author_data)
        return book

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        authors = instance.authors.all()
        authors = [author.name for author in authors]
        # if validated_data.get("authors", None):
        #     v_authors = validated_data.get("authors")
        #     v_authors = [author["name"] for author in v_authors]
            
        instance.country = validated_data.get('country', instance.country)
        instance.number_of_pages = validated_data.get('number_of_pages', instance.number_of_pages)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.save()
        return instance
