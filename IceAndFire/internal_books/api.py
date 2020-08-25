from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from internal_books.models import Book, Author
from .serializers import BookSerializer


class ResponseInfo(object):
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

    queryset = Book.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]

    def create(self, request):
        authors = request.data.pop('authors')
        book = Book.objects.create(**request.data)
        book_serialized = BookSerializer(book)
        for author in authors:
            Author.objects.create(book=book, name=author)
        response_format = ResponseInfo(status_code=201,
                                       status="success",
                                       data=book_serialized.data).response
        return Response(response_format)

    def list(self, request):
        serializer = BookSerializer(self.queryset, many=True)
        response_format = ResponseInfo(status_code=200,
                                       status="success",
                                       data=serializer.data).response
        return Response(response_format)

    def partial_update(self, request, pk=None):
        book = get_object_or_404(self.queryset, pk=pk)
        message = f"The book {str(book.name)} was updated successfully"

        book.name = self.update_data(request, 'name', book.name)
        book.isbn = self.update_data(request, 'isbn', book.isbn)
        book.country = self.update_data(request, 'country', book.country)
        book.number_of_pages = self.update_data(request, 'number_of_pages', book.number_of_pages)
        book.publisher = self.update_data(request, 'publisher', book.publisher)
        book.release_date = self.update_data(request, 'release_date', book.release_date)
        self.update_authors(request, book)
        
        book.save()
        serialized_book = BookSerializer(book)
        response_format = ResponseInfo(status_code=200,
                                       status="success",
                                       message=message,
                                       data=serialized_book.data).response

        return Response(response_format)

    def destroy(self, request, pk=None):
        book = get_object_or_404(self.queryset, pk=pk)
        message = f"The book {str(book.name)} was deleted successfully"
        authors = book.authors.all()
        for author in authors:
            author.delete()
        book.delete()
        response_format = ResponseInfo(status_code=200,
                                       status="success",
                                       message=message).response
        return Response(response_format)

    def retrieve(self, request, pk=None):
        book = get_object_or_404(self.queryset, pk=pk)
        book_serialized = BookSerializer(book)

        response_format = ResponseInfo(status_code=200,
                                       status="success",
                                       data=book_serialized.data).response
        return Response(response_format)

    def update_data(self, request, attr, prev_value):
        return request.data.get(attr, prev_value)

    def update_authors(self, request, book):
        authors = book.authors.all()
        updated_authors = request.data.get("authors",)

        if not updated_authors:
            return

        min_len_author = min(len(authors), len(updated_authors))
        for i in range(min_len_author):
            authors[i].name = updated_authors[i]
            authors[i].save()
        if len(authors) > len(updated_authors):
            for i in range(len(updated_authors), len(authors)):
                authors[i].delete()
        elif len(authors) < len(updated_authors):
            for i in range(len(authors), len(updated_authors)):
                Author.objects.create(book=book, name=updated_authors[i])
