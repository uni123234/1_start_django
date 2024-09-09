from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    LogoutUserView,
    RegisterView,
    LoginView,
    SchoolListView,
    StudentListView,
    TeacherListView,
    CreateStudentView,
    UpdateStudentView,
    CreateClassView,
    UpdateClassView,
    CreateSchoolView,
    UpdateSchoolView,
    CreateTeacherView,
    UpdateTeacherView,
    ClassListView,
    SearchNameView,
    EditUserView,
    EditProfileView,
)

app_name = "myapp"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("students/", StudentListView.as_view(), name="student_list"),
    path("teachers/", TeacherListView.as_view(), name="teacher_list"),
    path("create_student/", CreateStudentView.as_view(), name="create_student"),
    path("edit_student/<int:pk>/", UpdateStudentView.as_view(), name="edit_student"),
    path("create_teacher/", CreateTeacherView.as_view(), name="create_teacher"),
    path("edit_teacher/<int:pk>/", UpdateTeacherView.as_view(), name="edit_teacher"),
    path("class_list/", ClassListView.as_view(), name="class_list"),
    path("create_class/", CreateClassView.as_view(), name="create_class"),
    path("edit_class/<int:pk>/", UpdateClassView.as_view(), name="edit_class"),
    path("school_list/", SchoolListView.as_view(), name="school_list"),
    path("create_school/", CreateSchoolView.as_view(), name="create_school"),
    path("edit_school/<int:pk>/", UpdateSchoolView.as_view(), name="edit_school"),
    path("profile/", EditUserView.as_view(), name="profile"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("teachers/search/", SearchNameView.as_view(), name="search_teacher_name"),
]
