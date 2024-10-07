from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookListCreateView, BookDetailView, GenerateBooksView

app_name = "lib"

router = DefaultRouter()
router.register(r"books", BookListCreateView, basename="book-list-create")

urlpatterns = [
    path("", include(router.urls)),
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path(
        "generate-books/", GenerateBooksView.as_view(), name="generate-books"
    ),
]
