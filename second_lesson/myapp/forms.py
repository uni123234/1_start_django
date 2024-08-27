from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
)
from .models import Student, Subject, Teacher, Class, CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new custom user."""

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "is_teacher", "is_student"]


class CustomUserChangeForm(UserChangeForm):
    """Form for editing a custom user."""

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]


class UserLoginForm(AuthenticationForm):
    """Form for logging in a user."""

    username = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    # No Meta class needed here as AuthenticationForm does not use model


class ProfileForm(forms.ModelForm):
    """Form for editing a user's profile."""

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]


class StudentForm(forms.ModelForm):
    """Form for creating or editing a student."""

    class Meta:
        model = Student
        fields = ["first_name", "last_name", "address", "school", "class_number"]


class TeacherForm(forms.ModelForm):
    """Form for creating or editing a teacher."""

    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "email", "school"]


class ClassForm(forms.ModelForm):
    """Form for creating or editing a class."""

    favorite_subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Class
        fields = ["school", "class_number", "location", "favorite_subjects"]
