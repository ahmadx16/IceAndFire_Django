from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestExternalBooks(APITestCase):
    """Tests API of external_books"""

    def test_get_external_book(self):
        # A valid book url
        url = '%s?name=A Game of Thrones' % reverse('external-book')
        response = self.client.get(url)
        expected_response_data = [
            {
                "name": "A Game of Thrones",
                "isbn": "978-0553103540",
                "authors": [
                    "George R. R. Martin"
                ],
                "publisher": "Bantam Books",
                "country": "United States",
                "number_of_pages": 694,
                "release_date": "1996-08-01"
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response_data)
       
        # url with non-existing book
        url = '%s?name=Not a book' % reverse('external-book')
        response = self.client.get(url)
        expected_response_data = []
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response_data)
