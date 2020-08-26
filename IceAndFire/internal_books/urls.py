from rest_framework import routers
from .api import BookViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register('books', BookViewSet, 'internal-book')

urlpatterns = router.urls
