from django.urls import path
import requests

from .api import ExternalBook


urlpatterns = [
    path('', ExternalBook.as_view(), name='external-book')
]
