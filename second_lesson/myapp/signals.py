from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Teacher, Student


@receiver([post_save, post_delete], sender=Teacher)
def clear_teacher_cache(sender, instance, **kwargs):
    cache.delete("all_teachers")


@receiver([post_save, post_delete], sender=Student)
def clear_student_cache(sender, instance, **kwargs):
    cache.delete("all_students")
