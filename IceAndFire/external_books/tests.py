from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestExternalBooks(APITestCase):
    """Tests API of external_books"""

    def test_get_external_book(self):
        # A valid book url
        url = f"{reverse('external-book')}?name=A Game of Thrones"

        book_response = self.client.get(url)
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
        self.assertEqual(book_response.status_code, status.HTTP_200_OK)
        self.assertEqual(book_response.data, expected_response_data)

        # url with non-existing book
        url = f"{reverse('external-book')}?name=Not A Book"
        book_response = self.client.get(url)
        expected_response_data = []
        self.assertEqual(book_response.status_code, status.HTTP_200_OK)
        self.assertEqual(book_response.data, expected_response_data)
