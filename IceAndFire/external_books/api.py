from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
import datetime as dt

from .serializers import ExternalBookSerializer


class ExternalBook(APIView):
    """Book data from external API"""

    external_url = "https://www.anapioficeandfire.com/api/books"

    def get(self, request):
        try:
            if request.query_params.get("name",):
                url = self.external_url + "?name=" + request.query_params.get("name",)
            else:
                url = self.external_url
            response = requests.request("GET", url)
        except requests.exceptions.Timeout:
            error = {"error": "Connection Timeout, Check your connection"}
            return Response(error, status=status.HTTP_408_REQUEST_TIMEOUT)
        except requests.exceptions.ConnectionError:
            error = {"error": "No Connection, Check your connection"}
            return Response(error, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        response_books = response.json()
        serializer = ExternalBookSerializer(data=response_books, many=True)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
