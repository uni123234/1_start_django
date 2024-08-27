from django import forms
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from .models import Class, Student, Teacher
from .forms import (
    CustomUserChangeForm,
    ProfileForm,
    StudentForm,
    UserLoginForm,
    CustomUserCreationForm,
    TeacherForm,
)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_teacher = "is_teacher" in request.POST
            is_student = "is_student" in request.POST

            if not is_teacher and not is_student:
                messages.error(
                    request, "You must select at least one role (teacher or student)."
                )
                return render(request, "register.html", {"form": form})

            user.is_teacher = is_teacher
            user.is_student = is_student
            user.save()

            messages.success(request, f"Account created for {user.email}!")
            login(request, user)
            if user.is_teacher:
                return redirect("myapp:teacher_list")
            else:
                return redirect("myapp:student_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {email}!")
                if user.is_teacher:
                    return redirect("myapp:teacher_list")
                else:
                    return redirect("myapp:student_list")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form})


@login_required
def student_list(request):
    if not request.user.is_teacher:
        raise PermissionDenied("You do not have permission to view this page.")
    students = Student.objects.all()
    paginator = Paginator(students, 10)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)
    return render(request, "index.html", {"page_obj": page_obj})


@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    paginator = Paginator(teachers, 10)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)
    return render(request, "teacher_list.html", {"page_obj": page_obj})


@login_required
def create_students(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("myapp:student_list")
    else:
        form = StudentForm()
    return render(request, "create_students.html", {"form": form})


@login_required
def edit_students(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("myapp:student_list")
    else:
        form = StudentForm(instance=student)
    return render(request, "edit_students.html", {"form": form})


def class_list(request):
    classes = Class.objects.all()
    return render(request, "class_list.html", {"classes": classes})


@login_required
def create_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("myapp:teacher_list")
    else:
        form = TeacherForm()
    return render(request, "create_teacher.html", {"form": form})


@login_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("myapp:teacher_list")
    else:
        form = TeacherForm(instance=teacher)
    return render(request, "edit_teacher.html", {"form": form})


def search_name(request):
    query = request.GET.get("query", "")
    if query:
        students = Student.objects.filter(
            first_name__icontains=query
        ) | Student.objects.filter(last_name__icontains=query)
        teachers = Teacher.objects.filter(
            first_name__icontains=query
        ) | Teacher.objects.filter(last_name__icontains=query)
        results = list(students.values_list("first_name", "last_name")) + list(
            teachers.values_list("first_name", "last_name")
        )
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


def search_teacher_name(request):
    query = request.GET.get("query", "")
    if query:
        teachers = Teacher.objects.search_by_name(query)
        names = [f"{teacher.first_name} {teacher.last_name}" for teacher in teachers]
    else:
        names = []

    return JsonResponse(names, safe=False)


@login_required
def profile_view(request):
    user = request.user
    menu = {
        "Profile": reverse_lazy("myapp:profile"),
        "Edit Profile": reverse_lazy("myapp:edit_profile"),
        "Logout": reverse_lazy("myapp:logout"),
    }
    return render(request, "profile.html", {"user": user, "menu": menu})


@login_required
def edit_user(request):
    user = request.user
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been updated!")
            return redirect("myapp:profile")
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, "edit_user.html", {"user_form": form})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("myapp:profile")
    else:
        form = ProfileForm(instance=user)
    return render(request, "edit_profile.html", {"profile_form": form})
