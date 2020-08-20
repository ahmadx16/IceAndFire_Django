from rest_framework import viewsets, permissions

from internal_books.models import Book
from .serializers import BookSerializer


# book viewset
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = BookSerializer