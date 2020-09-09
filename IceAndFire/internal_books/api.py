from rest_framework import status, generics, filters
from rest_framework.response import Response
from .models.book import Book
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
        book_json = super().list(request, *args, **kwargs)
        formatted_response = ResponseInfo(status_code=200,
                                          status="success",
                                          data=book_json.data).response
        return Response(formatted_response)

    def create(self, request, *args, **kwargs):
        book_json = super().create(request, *args, **kwargs)
        formatted_response = ResponseInfo(status_code=201,
                                          status="success",
                                          data=book_json.data).response
        return Response(formatted_response, status=status.HTTP_201_CREATED)


class BookRetrieveUpdateDestroyView(BookQuerySet, generics.RetrieveUpdateDestroyAPIView):
    """For handeling internal books Retrieve, Update, Destroy functionality"""

    def retrieve(self, request, *args, **kwargs):
        book_json = super().retrieve(request, *args, **kwargs)
        formatted_response = ResponseInfo(status_code=200,
                                          status="success",
                                          data=book_json.data).response
        return Response(formatted_response)

    def update(self, request, *args, **kwargs):
        book_obj = self.get_object()
        previous_book_name = str(book_obj.name)
        book_json = super().update(request, *args, **kwargs)
        message = "The book {} was updated successfully".format(previous_book_name)
        formatted_response = ResponseInfo(status_code=200,
                                          status="success",
                                          message=message,
                                          data=book_json.data).response
        return Response(formatted_response)

    def destroy(self, request, *args, **kwargs):
        book_obj = self.get_object()
        book_name = str(book_obj.name)
        authors = list(book_obj.authors.all())
        super().destroy(request, *args, **kwargs)
        for author in authors:
            # checks and remove authors with no books
            author.remove_extra_author()
        message = f"The book {book_name} was deleted successfully"
        formatted_response = ResponseInfo(status_code=200,
                                          status="success",
                                          message=message).response
        return Response(formatted_response)
