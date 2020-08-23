from rest_framework import viewsets, permissions
from rest_framework.response import Response

from internal_books.models import Book
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


class BookViewSet(viewsets.ModelViewSet):
    """Book ViewSet for handeling internal books"""

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(BookViewSet, self).__init__(**kwargs)

    queryset = Book.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        create_response = super(BookViewSet, self).create(request, *args, **kwargs)
        response_format = ResponseInfo(status_code=201,
                                       status="success",
                                       data=create_response.data).response
        return Response(response_format)

    def list(self, request, *args, **kwargs):
        list_response = super(BookViewSet, self).list(request, *args, **kwargs)
        response_format = ResponseInfo(status_code=200,
                                       status="success",
                                       data=list_response.data).response
        return Response(response_format)

    def update(self, request, *args, **kwargs):
        update_response = super(BookViewSet, self).update(request, *args, **kwargs)
        book_name = update_response.data["name"]
        message = f"The book {book_name} was updated successfully"
        response_format = ResponseInfo(status_code=200,
                                       status="success",
                                       message=message,
                                       data=update_response.data).response

        return Response(response_format)

    def destroy(self, request, *args, **kwargs):

        book_instance = self.get_object()
        book_name = self.get_serializer(book_instance).data["name"]
        message = f"The book {book_name} was deleted successfully"
        destroy_response = super(BookViewSet, self).destroy(request, *args, **kwargs)
        response_format = ResponseInfo(status_code=200,
                                       status="success",
                                       message=message).response

        return Response(response_format)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.response_format["status_code"] = 200
        self.response_format["status"] = "success"
        self.response_format["data"].append(serializer.data)
        return Response(self.response_format)

    # def destroy(self, request, *args, **kwargs):
