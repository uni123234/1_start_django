# myapp/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'myapp'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('students/', views.student_list, name='student_list'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('create_student/', views.create_students, name='create_students'),
    path('edit_student/<int:student_id>/', views.edit_students, name='edit_students'),
    path('create_teacher/', views.create_teacher, name='create_teacher'),
    path('edit_teacher/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search_teacher/', views.search_teacher_name, name='search_teacher_name'),
    path('search/', views.search_name, name='search_name'),
    path('class_list/', views.class_list, name='class_list'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
