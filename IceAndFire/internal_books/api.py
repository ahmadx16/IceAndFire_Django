from rest_framework import viewsets
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
    # permissions_classes = [
    #     permissions.AllowAny
    # ]

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

    def list(self, request, *args, **kwargs):
        serializer = BookSerializer(self.queryset, many=True)
        response_format = ResponseInfo(status_code=200,
                                       status="success",
                                       data=serializer.data).response
        return Response(response_format)

    # def update(self, request, *args, **kwargs):
    #     update_response = super(BookViewSet, self).update(request, *args, **kwargs)
    #     book_name = update_response.data["name"]
    #     message = f"The book {book_name} was updated successfully"
    #     response_format = ResponseInfo(status_code=200,
    #                                    status="success",
    #                                    message=message,
    #                                    data=update_response.data).response

    #     return Response(response_format)

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
