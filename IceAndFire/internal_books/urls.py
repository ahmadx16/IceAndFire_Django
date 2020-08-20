from rest_framework import routers
from .api import BookViewSet


router = routers.DefaultRouter()
router.register('api/v1/books', BookViewSet, 'internal_books')

urlpatterns = router.urls
