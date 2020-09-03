from rest_framework import viewsets, status, generics
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


class BookListCreateView(generics.ListCreateAPIView):
    """For handeling internal books List, Create functionality"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer

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
        return Response(formatted_response)


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """For handeling internal books Retrieve, Update, Destroy functionality"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
