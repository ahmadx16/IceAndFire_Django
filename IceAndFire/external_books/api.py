from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests

from .serializers import ExternalBookSerializer


class ExternalBook(APIView):
    """Book data from external API"""

    external_url = "https://www.anapioficeandfire.com/api/books"

    def get(self, request):
        try:
            book_response = requests.request("GET", self.external_url, params=request.query_params)
        except requests.exceptions.Timeout:
            error = {"error": "Connection Timeout, Check your connection"}
            return Response(error, status=status.HTTP_408_REQUEST_TIMEOUT)
        except requests.exceptions.ConnectionError:
            error = {"error": "No Connection, Check your connection"}
            return Response(error, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        book_response = book_response.json()
        book_serializer = ExternalBookSerializer(data=book_response, many=True)

        if book_serializer.is_valid():
            return Response(book_serializer.data)

        return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
