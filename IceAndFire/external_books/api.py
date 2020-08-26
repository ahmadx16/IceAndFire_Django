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
                if request.query_params.get("name",) == book.get("name"):
                    relevent_books.append(book)
            return Response(relevent_books)

        return Response(serializer.errors)
