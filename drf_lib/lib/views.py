from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer
from .tasks import send_new_book_notification
from .factories import BookFactory


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["author", "published_date"]
    search_fields = ["title", "author"]
    ordering_fields = ["title", "published_date"]
    ordering = ["published_date"]

    def perform_create(self, serializer):
        book = serializer.save()
        send_new_book_notification.delay(book.id)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        instance.delete()


class GenerateBooksView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        num_books = int(request.data.get("num_books", 10))
        BookFactory.create_batch(num_books)
        return Response({"message": f"Successfully created {num_books} books."})
