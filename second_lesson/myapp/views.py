from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView, CreateView, UpdateView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db.models import Q
from django.db import transaction
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
            default_class, created = Class.objects.get_or_create(
                name="Default Teacher Class",
                defaults={
                    "location": "Default Location",
                    "school": user.school,
                },
            )
            user.default_class = default_class
            user.save()

        if user.is_student:
            default_class, created = Class.objects.get_or_create(
                name="Default Student Class",
                defaults={
                    "location": "Default Location",
                    "school": user.school,
                },
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
        return redirect(
            "myapp:teacher_list" if user.is_teacher else "myapp:student_list"
        )

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error with your registration. Please check the form and try again.",
        )
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
                return redirect(
                    "myapp:teacher_list" if user.is_teacher else "myapp:student_list"
                )
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(
                request, "There was an error with the form. Please check the inputs."
            )
        return render(request, "login.html", {"form": form})


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "index.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):
        if not self.request.user.is_teacher:
            messages.error(
                self.request, "You do not have permission to view this page."
            )
            raise PermissionDenied("You do not have permission to view this page.")
        return Student.objects.all()


class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = "teacher_list.html"
    context_object_name = "teachers"
    paginate_by = 10

    def get_queryset(self):
        return Teacher.objects.order_by("last_name")


class CreateStudentView(LoginRequiredMixin, CreateView):
    form_class = StudentForm
    template_name = "create_students.html"
    success_url = reverse_lazy("myapp:student_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Student has been created successfully!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error with the form. Please check the inputs."
        )
        return self.render_to_response(self.get_context_data(form=form))


class UpdateStudentView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "edit_students.html"
    success_url = reverse_lazy("myapp:student_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Student has been updated successfully!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error updating the student. Please check the form and try again.",
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        return Student.objects.get(pk=self.kwargs["pk"])

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

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error with the form. Please check the inputs."
        )
        return self.render_to_response(self.get_context_data(form=form))


class UpdateClassView(LoginRequiredMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = "edit_class.html"
    success_url = reverse_lazy("myapp:class_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Class has been updated successfully!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error updating the class. Please check the form and try again.",
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        return Class.objects.get(pk=self.kwargs["pk"])


class CreateSchoolView(LoginRequiredMixin, CreateView):
    form_class = SchoolForm
    template_name = "create_school.html"
    success_url = reverse_lazy("myapp:school_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "School has been created successfully!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error with the form. Please check the inputs."
        )
        return self.render_to_response(self.get_context_data(form=form))


class UpdateSchoolView(LoginRequiredMixin, UpdateView):
    model = School
    form_class = SchoolForm
    template_name = "edit_school.html"
    success_url = reverse_lazy("myapp:school_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "School has been updated successfully!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error updating the school. Please check the form and try again.",
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        return School.objects.get(pk=self.kwargs["pk"])


class CreateTeacherView(LoginRequiredMixin, CreateView):
    form_class = TeacherForm
    template_name = "create_teacher.html"
    success_url = reverse_lazy("myapp:teacher_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Teacher has been created successfully!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error with the form. Please check the inputs."
        )
        return self.render_to_response(self.get_context_data(form=form))


class UpdateTeacherView(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "edit_teacher.html"
    success_url = reverse_lazy("myapp:teacher_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Teacher has been updated successfully!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error updating the teacher. Please check the form and try again.",
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        return Teacher.objects.get(pk=self.kwargs["pk"])


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
            results = Student.objects.filter(Q(name__icontains=query)).values("name")
        return JsonResponse(list(results), safe=False)


class EditUserView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "edit_user.html"
    success_url = reverse_lazy("myapp:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "User profile has been updated successfully!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error updating the profile. Please check the form and try again.",
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
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

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Profile has been updated successfully!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error updating the profile. Please check the form and try again.",
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
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


class SaveClassView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return JsonResponse({"error": "Permission denied."}, status=403)

        class_id = kwargs.get("class_id")
        class_obj = get_object_or_404(Class, id=class_id)

        teacher = request.user.teacher

        if class_obj in teacher.saved_classes.all():
            teacher.saved_classes.remove(class_obj)
            return JsonResponse({"message": "Class unsaved."}, status=200)
        else:
            teacher.saved_classes.add(class_obj)
            return JsonResponse({"message": "Class saved."}, status=200)


class LogoutUserView(LogoutView):
    next_page = reverse_lazy("myapp:login")
