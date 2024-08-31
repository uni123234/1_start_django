from django.shortcuts import redirect, render
from django.views.generic import View, ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Class, CustomUser, School, Student, Teacher
from .forms import (
    ClassForm,
    CustomUserChangeForm,
    ProfileForm,
    SchoolForm,
    StudentForm,
    UserLoginForm,
    CustomUserCreationForm,
    TeacherForm,
)


def handle_user_roles(user, request):
    """
    Set user roles and handle additional setup based on user type.
    """
    with transaction.atomic():
        if user.is_teacher:
            try:
                default_class = Class.objects.get(name="Default Teacher Class")
            except ObjectDoesNotExist:
                default_class = Class.objects.create(
                    name="Default Teacher Class",
                    location="Default Location",
                    school=user.school,
                )
            user.default_class = default_class
            user.save()

        if user.is_student:
            try:
                default_class = Class.objects.get(name="Default Student Class")
            except ObjectDoesNotExist:
                default_class = Class.objects.create(
                    name="Default Student Class",
                    location="Default Location",
                    school=user.school,
                )
            user.classes.add(default_class)
            user.save()


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "register.html"

    def form_valid(self, form):
        user = form.save()
        handle_user_roles(user, self.request)
        login(self.request, user)
        messages.success(self.request, f"Welcome, {user.email}!")
        if user.is_teacher:
            return redirect("myapp:teacher_list")
        return redirect("myapp:student_list")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.email}!")
                if user.is_teacher:
                    return redirect("myapp:teacher_list")
                return redirect("myapp:student_list")
            else:
                messages.error(request, "Invalid email or password.")
        return render(request, "login.html", {"form": form})


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "index.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):
        if not self.request.user.is_teacher:
            raise PermissionDenied("You do not have permission to view this page.")
        return Student.objects.all()


class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = "teacher_list.html"
    context_object_name = "teachers"
    paginate_by = 10


class CreateStudentView(LoginRequiredMixin, CreateView):
    form_class = StudentForm
    template_name = "create_students.html"
    success_url = reverse_lazy("myapp:student_list")


class UpdateStudentView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "edit_students.html"
    success_url = reverse_lazy("myapp:student_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit_url"] = reverse(
            "myapp:edit_student", kwargs={"pk": self.object.pk}
        )
        return context


class CreateClassView(LoginRequiredMixin, CreateView):
    form_class = ClassForm
    template_name = "create_class.html"
    success_url = reverse_lazy("myapp:class_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Class has been created successfully!")
        return response


class UpdateClassView(LoginRequiredMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = "edit_class.html"
    success_url = reverse_lazy("myapp:class_list")


class CreateSchoolView(LoginRequiredMixin, CreateView):
    form_class = SchoolForm
    template_name = "create_school.html"
    success_url = reverse_lazy("myapp:school_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "School has been created successfully!")
        return response


class UpdateSchoolView(LoginRequiredMixin, UpdateView):
    model = School
    form_class = SchoolForm
    template_name = "edit_school.html"
    success_url = reverse_lazy("myapp:school_list")


class CreateTeacherView(LoginRequiredMixin, CreateView):
    form_class = TeacherForm
    template_name = "create_teacher.html"
    success_url = reverse_lazy("myapp:teacher_list")


class UpdateTeacherView(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "edit_teacher.html"
    success_url = reverse_lazy("myapp:teacher_list")


class ClassListView(LoginRequiredMixin, ListView):
    model = Class
    template_name = "class_list.html"
    context_object_name = "classes"


class SchoolListView(LoginRequiredMixin, ListView):
    model = School
    template_name = "school_list.html"
    context_object_name = "schools"


class SearchNameView(View):
    def get(self, request):
        query = request.GET.get("query", "")
        results = []
        if query:
            students = Student.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
            teachers = Teacher.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
            results = list(students.values_list("first_name", "last_name")) + list(
                teachers.values_list("first_name", "last_name")
            )
        return JsonResponse(results, safe=False)


class SearchTeacherNameView(View):
    def get(self, request):
        query = request.GET.get("query", "")
        if query:
            teachers = Teacher.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
            names = [
                f"{teacher.first_name} {teacher.last_name}" for teacher in teachers
            ]
        else:
            names = []
        return JsonResponse(names, safe=False)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["menu"] = {
            "Profile": reverse_lazy("myapp:profile"),
            "Edit Profile": reverse_lazy("myapp:edit_profile"),
            "Logout": reverse_lazy("myapp:logout"),
            "Edit Students": reverse_lazy(
                "myapp:edit_student", kwargs={"pk": self.request.user.pk}
            ),
        }
        return context


class EditUserView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "edit_user.html"
    success_url = reverse_lazy("myapp:profile")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = self.get_form()
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = "edit_profile.html"
    success_url = reverse_lazy("myapp:profile")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_form"] = self.get_form()
        context["menu"] = {
            "Profile": reverse_lazy("myapp:profile"),
            "Edit Profile": reverse_lazy("myapp:edit_profile"),
            "Logout": reverse_lazy("myapp:logout"),
        }
        return context


class CustomLogoutView(LogoutView):
    http_method_names = ["get", "post"]
    next_page = None

    def get_redirect_url(self):
        return self.next_page or reverse("myapp:login")
