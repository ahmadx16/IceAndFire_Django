from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
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
            for author in authors:
                Author.objects.create(book=book, **author)

            book_serialized = BookSerializer(book)
            formated_response = ResponseInfo(status_code=201,
                                             status="success",
                                             data=[{"book": book_serialized.data}]).response
            return Response(formated_response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if request.query_params:
            books_query = Book.objects.filter(Q(name=request.query_params.get("name",))
                                              | Q(country=request.query_params.get("country",))
                                              | Q(publisher=request.query_params.get("publisher",))
                                              | Q(release_date__startswith=request.query_params
                                                  .get("release_date", "None"))
                                              )
        else:
            books_query = Book.objects.all()
        serializer = BookSerializer(books_query, many=True)
        formated_response = ResponseInfo(status_code=200,
                                         status="success",
                                         data=serializer.data).response
        return Response(formated_response)

    def partial_update(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        book_name = str(book.name)

        serializer = BookSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            authors = validated_data.pop('authors', None)
            # updating authors if given in request
            self.update_authors(authors, book)
            # updating to new values from request
            for (key, value) in validated_data.items():
                setattr(book, key, value)
            book.save()

            serialized_book = BookSerializer(book)
            message = f"The book {str(book_name)} was updated successfully"

            formated_response = ResponseInfo(status_code=200,
                                             status="success",
                                             message=message,
                                             data=serialized_book.data).response
            return Response(formated_response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        message = f"The book {str(book.name)} was deleted successfully"
        book.delete()

        formated_response = ResponseInfo(status_code=200,
                                         status="success",
                                         message=message).response
        return Response(formated_response)

    def retrieve(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        book_serialized = BookSerializer(book)

        formated_response = ResponseInfo(status_code=200,
                                         status="success",
                                         data=book_serialized.data).response
        return Response(formated_response)

    def update_authors(self, updated_authors, book):
        """Updates authors of a given book instance."""

        if not updated_authors:
            return

        updated_authors = [author["name"] for author in updated_authors]

        # delete previous authors
        book.authors.all().delete()
        # create new authors referencing to same book
        for author in updated_authors:
            Author.objects.create(book=book, name=author)
