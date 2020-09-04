from rest_framework import routers
from django.urls import path
from .api import BookListCreateView, BookRetrieveUpdateDestroyView


urlpatterns = [
    path('books', BookListCreateView.as_view(), name='internal-book-list'),
    path('books/<int:pk>', BookRetrieveUpdateDestroyView.as_view(), name='internal-book-detail')
]
