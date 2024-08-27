from django import template
from django.urls import reverse_lazy
from myapp.models import Student, Teacher, Class

register = template.Library()

@register.simple_tag
def total_students():
    return Student.objects.count()

@register.simple_tag
def total_teachers():
    return Teacher.objects.count()

@register.simple_tag
def total_classes():
    return Class.objects.count()

@register.inclusion_tag("tags/profile_menu.html")
def profile_menu(user, school_id=None, student_id=None, teacher_id=None):
    menu = {}
    if user.is_teacher:
        menu = {
            "Profile": reverse_lazy("myapp:profile"),
            "Edit User": reverse_lazy("myapp:edit_user"),
            "Edit Profile": reverse_lazy("myapp:edit_profile"),
            "Edit Class": reverse_lazy("myapp:class_list"),
            "Edit School": (
                reverse_lazy("myapp:edit_school", kwargs={'pk': school_id})
                if school_id
                else None
            ),
            "Edit Student": (
                reverse_lazy("myapp:edit_student", kwargs={'pk': student_id})
                if student_id
                else None
            ),
            "Edit Teacher": (
                reverse_lazy("myapp:edit_teacher", kwargs={'pk': teacher_id})
                if teacher_id
                else None
            ),
            "Create Student": reverse_lazy("myapp:create_student"),
            "Create Teacher": reverse_lazy("myapp:create_teacher"),
            "Create Class": reverse_lazy("myapp:create_class"),
            "Create School": reverse_lazy("myapp:create_school"),
        }
    elif user.is_student:
        menu = {
            "Profile": reverse_lazy("myapp:profile"),
            "Edit User": reverse_lazy("myapp:edit_user"),
            "Edit Profile": reverse_lazy("myapp:edit_profile"),
        }
    return {"menu": {k: v for k, v in menu.items() if v is not None}}
