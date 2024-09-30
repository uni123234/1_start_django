from celery import shared_task
from django.core.mail import send_mail
from .models import Book


@shared_task
def send_new_book_notification(book_id):

    book = Book.objects.get(id=book_id)
    send_mail(
        "Нова книга додана",
        f'Книга "{book.title}" була додана в систему.',
        "admin@example.com",
        ["user@example.com"],
        fail_silently=False,
    )
