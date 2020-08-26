from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import datetime as dt

from .serializers import ExternalBookSerializer


class ExternalBook(APIView):
    """Book data from external API"""

    external_url = "https://www.anapioficeandfire.com/api/books"

    def get(self, request):
        try:
            response = requests.request("GET", self.external_url)
        except requests.exceptions.RequestException as error:
            exit("Cannot connect at the moment")

        response_books = response.json()

        serializer = ExternalBookSerializer(data=response_books, many=True)

        if serializer.is_valid():
            books = serializer.data
            relevent_books = []
            for book in books:
                if self.is_book_relevent(book, request.query_params):
                    relevent_books.append(book)
            return Response(relevent_books)

        return Response(serializer.errors)

    def is_book_relevent(self, book, params):
        """Returns True if the given book is relevent to query"""
        
        if not params:
            return True

        check_params = (
            "name",
            "country",
            "publisher"
        )
        for check_param in check_params:
            if params.get(check_param,) == book.get(check_param):
                return True

        year = dt.datetime.strptime(book.get("release_date"), "%Y-%m-%d").strftime("%Y")

        return year == params.get("release_date",)
