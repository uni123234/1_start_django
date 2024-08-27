from django import template
from django.core.paginator import Paginator
from ..models import Student, Teacher
from django.urls import reverse_lazy

register = template.Library()

@register.simple_tag
def total_students():
    return Student.objects.count()

@register.simple_tag
def total_teachers():
    return Teacher.objects.count()

@register.inclusion_tag("students_pagination.html", takes_context=True)
def students_pagination(context, students, page_num):
    paginator = Paginator(students, 10)
    page_obj = paginator.get_page(page_num)
    return {"page_obj": page_obj, "request": context["request"]}

@register.inclusion_tag('tags/profile_menu.html')
def profile_menu(user):
    menu = {}
    if user.is_teacher:
        menu = {
            'Profile': reverse_lazy('myapp:profile'),
            'Edit User': reverse_lazy('myapp:edit_user'),
            'Edit Profile': reverse_lazy('myapp:edit_profile'),
            'View Students': reverse_lazy('myapp:student_list'),
            'Create Student': reverse_lazy('myapp:create_students'),
            'Create Teacher': reverse_lazy('myapp:create_teacher'),
        }
    elif user.is_student:
        menu = {
            'Profile': reverse_lazy('myapp:profile'),
            'Edit User': reverse_lazy('myapp:edit_user'),
            'Edit Profile': reverse_lazy('myapp:edit_profile'),
        }
    return {'menu': menu}
