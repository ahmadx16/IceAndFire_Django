from rest_framework import routers
from django.urls import path
from .api import BookListCreateView, BookRetrieveUpdateDestroyView


urlpatterns = [
    path('books', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>', BookRetrieveUpdateDestroyView.as_view(), name='book-list-create')
]
