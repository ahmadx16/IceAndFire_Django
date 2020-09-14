from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('api/v1/', include('internal_books.urls')),
    path('api/external-books/', include('external_books.urls')),

]
