from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from .serializers import ExternalBookSerializer


class ExternalBook(APIView):
    """Book data from external API"""

    external_url = "https://www.anapioficeandfire.com/api/books"

    def get(self, request):
        try:
            response = requests.request("GET", self.external_url)
        except:
            print("Cannot connect at the moment")
        response = response.json()

        name = request.query_params.get("name",)
        final_response = []
        for resp in response:
            if resp.get("name") == name:
                final_response.append(resp)

        serializer = ExternalBookSerializer(data=final_response, many=True)
        if serializer.is_valid():
            return Response(serializer.data)

        return Response(serializer.errors)
