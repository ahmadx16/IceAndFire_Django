from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import datetime as dt
from rest_framework import status

from internal_books.models import Book, Author
from .serializers import BookSerializer


class ResponseInfo(object):
    """Corrects response format"""

    def __init__(self, **kwargs):
        self.response = {
            "status_code": kwargs.get("status_code",),
            "status": kwargs.get("status",),
            "message": kwargs.get("message",),
            "data": kwargs.get("data", [])
        }
        if not self.response.get("message"):
            self.response.pop("message")


class BookViewSet(viewsets.ViewSet):
    """Book ViewSet for handeling internal books"""

    def create(self, request):
        # validating data before creating user
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            authors = validated_data.pop('authors')
            book = Book.objects.create(**validated_data)
            book_serialized = BookSerializer(book)
            for author in authors:
                Author.objects.create(book=book, **author)

            response_format = ResponseInfo(status_code=201,
                                           status="success",
                                           data=[{"book": book_serialized.data}]).response
            return Response(response_format, status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

    def list(self, request):
        serializer = BookSerializer(Book.objects.all(), many=True)
        books = serializer.data
        # only books relevent to query of all books if no query
        relevent_books = []
        for book in books:
            if self.is_book_relevent(book, request.query_params):
                relevent_books.append(book)
        response_format = ResponseInfo(status_code=200,
                                       status="success",
                                       data=relevent_books).response
        return Response(response_format)

    def partial_update(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        message = f"The book {str(book.name)} was updated successfully"

        serializer = BookSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            self.update_book(validated_data, book)
            serialized_book = BookSerializer(book)

            response_format = ResponseInfo(status_code=200,
                                           status="success",
                                           message=message,
                                           data=serialized_book.data).response
            return Response(response_format)

        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        message = f"The book {str(book.name)} was deleted successfully"
        authors = book.authors.all()
        # deleting related authors of the book
        for author in authors:
            author.delete()
        book.delete()

        response_format = ResponseInfo(status_code=200,
                                       status="success",
                                       message=message).response
        return Response(response_format)

    def retrieve(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        book_serialized = BookSerializer(book)

        response_format = ResponseInfo(status_code=200,
                                       status="success",
                                       data=book_serialized.data).response
        return Response(response_format)

    def update_book(self, validated_data, book):
        """Updates the new fields if provided"""

        book.name = self.get_new_attr(validated_data, 'name', book.name)
        book.isbn = self.get_new_attr(validated_data, 'isbn', book.isbn)
        book.country = self.get_new_attr(validated_data, 'country', book.country)
        book.number_of_pages = self.get_new_attr(validated_data, 'number_of_pages', book.number_of_pages)
        book.publisher = self.get_new_attr(validated_data, 'publisher', book.publisher)
        book.release_date = self.get_new_attr(validated_data, 'release_date', book.release_date)
        self.update_authors(validated_data.get("authors",), book)

        book.save()

    def get_new_attr(self, validated_data, attr, prev_value):
        """Returns new attributes from request"""

        return validated_data.get(attr, prev_value)

    def update_authors(self, updated_authors, book):
        """Updates authors of a given book instance"""

        authors = book.authors.all()

        if not updated_authors:
            return

        updated_authors = [author["name"] for author in updated_authors]

        min_len_author = min(len(authors), len(updated_authors))
        for i in range(min_len_author):
            authors[i].name = updated_authors[i]
            authors[i].save()
        # if some authors removed from a book
        if len(authors) > len(updated_authors):
            for i in range(len(updated_authors), len(authors)):
                authors[i].delete()
        # if new authors added to book
        elif len(authors) < len(updated_authors):
            for i in range(len(authors), len(updated_authors)):
                Author.objects.create(book=book, name=updated_authors[i])

    def is_book_relevent(self, book, params):
        """Returns True if the given book is relevent to query"""

        if not params:
            return True

        check_params = (
            "name",
            "country",
            "publisher"
        )
        for check_param in check_params:
            # checks for the given parameter in the book
            if params.get(check_param,) == book.get(check_param):
                return True

        year = dt.datetime.strptime(book.get("release_date"), "%Y-%m-%d").strftime("%Y")

        # return true if year parameter matches in the book
        return year == params.get("release_date",)
