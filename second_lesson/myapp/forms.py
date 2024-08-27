from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from .models import School, Student, Subject, Teacher, Class, CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new custom user."""

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "is_teacher", "is_student"]

class CustomUserChangeForm(UserChangeForm):
    """Form for editing a custom user with optional password fields."""

    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"placeholder": "New Password"}),
        required=False
    )
    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm New Password"}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "The two password fields must match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")

        if password1:
            user.set_password(password1)

        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    """Form for logging in a user."""

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )

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

class SchoolForm(forms.ModelForm):
    """Form for creating or editing a school."""

    class Meta:
        model = School
        fields = ["name", "address", "school_number"]
