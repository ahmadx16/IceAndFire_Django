from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .test_data import expected_create_book, create_book_data, expected_read_book
from .test_data import update_book_data, expected_book_update
from .test_data import expected_delete_book


class TestInternalBooks(APITestCase):
    """Tests API of internal_books"""

    url_list = reverse('internal-book-list')

    def test_create_book_(self):
        """Tests create book API"""

        create_book_response = self.client.post(self.url_list, create_book_data, format='json')
        create_book_response.data["data"].pop("id")
        self.assertEqual(create_book_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_book_response.data, expected_create_book)

    def test_read_book_(self):
        """Tests read book API"""

        read_book_response = self.client.post(self.url_list, create_book_data, format='json')
        read_book_response = self.client.get(self.url_list)
        read_book_response.data["data"][0].pop("id")

        self.assertEqual(read_book_response.status_code, status.HTTP_200_OK)
        self.assertEqual(read_book_response.data, expected_read_book)

    def test_delete_book(self):
        """Tests update book API"""

        book_response = self.client.post(self.url_list, create_book_data, format='json')
        url_detial = reverse("internal-book-detail", kwargs={'pk': book_response.data['data']['id']})
        delete_book_response = self.client.delete(url_detial)

        self.assertEqual(delete_book_response.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_book_response.data, expected_delete_book)

    def test_update_book(self):
        """Tests update book API"""
        # auto scheduled to 4th
        book_response = self.client.post(self.url_list, create_book_data, format='json')
        url_detial = reverse("internal-book-detail", kwargs={'pk': book_response.data['data']['id']})
        update_book_response = self.client.patch(url_detial, update_book_data, format='json')
        update_book_response.data["data"].pop("id")

        self.assertEqual(update_book_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_book_response.data, expected_book_update)
