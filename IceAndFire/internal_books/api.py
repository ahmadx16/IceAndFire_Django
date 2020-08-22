from rest_framework import viewsets, permissions
from rest_framework.response import Response

from internal_books.models import Book
from .serializers import BookSerializer


class ResponseInfo(object):
    def __init__(self, **kwargs):
        self.response = {
            "status_code": kwargs.get("status_code",),
            "status": kwargs.get("status",),
            "data": kwargs.get("date", [])
        }


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
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.response_format["status_code"] = 200
        self.response_format["status"] = "success"
        self.response_format["data"].append(serializer.data)
        return Response(self.response_format)

    def list(self, request, *args, **kwargs):
        list_response = super(BookViewSet, self).list(request, *args, **kwargs)
        self.response_format["status_code"] = 200
        self.response_format["status"] = "success"
        self.response_format["data"] = list_response.data
        return Response(self.response_format)
