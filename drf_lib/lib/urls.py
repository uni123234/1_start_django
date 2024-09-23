from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

app_name = 'lib'

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
