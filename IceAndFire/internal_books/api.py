from rest_framework import status, generics, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Book
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


class BookQuerySet:
    """Defines queryset and serializer class for the book"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListCreateView(BookQuerySet, generics.ListCreateAPIView):
    """For handeling internal books List, Create functionality"""
    filter_backends = (filters.SearchFilter,)
    # case-insensitive partial searching
    search_fields = [
        'name',
        'publisher',
        'country',
        'release_date',
    ]

    def list(self, request, *args, **kwargs):
        books_response = super().list(request, *args, **kwargs)
        formatted_response = ResponseInfo(status_code=200,
                                          status="success",
                                          data=books_response.data).response
        return Response(formatted_response)

    def create(self, request, *args, **kwargs):
        books_response = super().create(request, *args, **kwargs)
        formatted_response = ResponseInfo(status_code=201,
                                          status="success",
                                          data=books_response.data).response
        return Response(formatted_response, status=status.HTTP_201_CREATED)


class BookRetrieveUpdateDestroyView(BookQuerySet, generics.RetrieveUpdateDestroyAPIView):
    """For handeling internal books Retrieve, Update, Destroy functionality"""

    def retrieve(self, request, *args, **kwargs):
        books_response = super().retrieve(request, *args, **kwargs)
        formatted_response = ResponseInfo(status_code=200,
                                          status="success",
                                          data=books_response.data).response
        return Response(formatted_response)

    def update(self, request, *args, **kwargs):
        books_response = super().update(request, *args, **kwargs)
        message = "The book {} was updated successfully".format(str(books_response.data['name']))
        formatted_response = ResponseInfo(status_code=200,
                                          status="success",
                                          message=message,
                                          data=books_response.data).response
        return Response(formatted_response)

    def destroy(self, request, *args, **kwargs):
        book_instance = self.get_object()
        book_name = str(book_instance.name)
        super().destroy(request, *args, **kwargs)
        message = f"The book {book_name} was deleted successfully"
        formatted_response = ResponseInfo(status_code=200,
                                          status="success",
                                          message=message).response
        return Response(formatted_response)
