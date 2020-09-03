from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Book, find_remove_extra_authors
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
        book_serializer = BookSerializer(data=request.data)
        if book_serializer.is_valid():
            book = book_serializer.save()
            serialized_book = BookSerializer(book)
            formatted_response = ResponseInfo(status_code=201,
                                              status="success",
                                              data=serialized_book.data).response
            return Response(formatted_response, status=status.HTTP_201_CREATED)

        return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        search_str = request.query_params.get('search_str',)
        if search_str:
            books_query = Book.objects.filter(Q(name__icontains=search_str)
                                              | Q(country__icontains=search_str)
                                              | Q(publisher__icontains=search_str)
                                              | Q(release_date__startswith=search_str)
                                              )
        else:
            books_query = Book.objects.all()
        serialized_books = BookSerializer(books_query, many=True)
        formatted_response = ResponseInfo(status_code=200,
                                          status="success",
                                          data=serialized_books.data).response
        return Response(formatted_response)

    def partial_update(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        book_name = str(book.name)

        book_serializer = BookSerializer(book, data=request.data, partial=True)
        if book_serializer.is_valid():
            updated_book = book_serializer.save()
            serialized_book = BookSerializer(updated_book)
            message = f"The book {str(book_name)} was updated successfully"

            formatted_response = ResponseInfo(status_code=200,
                                              status="success",
                                              message=message,
                                              data=serialized_book.data).response
            return Response(formatted_response)

        return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        book_name = book.name
        authors = list(book.authors.all())
        book.delete()
        find_remove_extra_authors(authors)
        message = f"The book {str(book_name)} was deleted successfully"
        formatted_response = ResponseInfo(status_code=200,
                                          status="success",
                                          message=message).response
        return Response(formatted_response)

    def retrieve(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        serialized_book = BookSerializer(book)

        formatted_response = ResponseInfo(status_code=200,
                                          status="success",
                                          data=serialized_book.data).response
        return Response(formatted_response)
