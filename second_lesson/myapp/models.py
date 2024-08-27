from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    school_number = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Class(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_number = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    favorite_subjects = models.ManyToManyField(Subject, related_name="classes")

    def __str__(self):
        return f"Class {self.class_number} at {self.school.name}"


class StudentManager(models.Manager):
    def search_by_name(self, query):
        return self.filter(first_name__icontains=query) | self.filter(
            last_name__icontains=query
        )


class TeacherManager(models.Manager):
    def search_by_name(self, query):
        return self.filter(first_name__icontains=query) | self.filter(
            last_name__icontains=query
        )


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_number = models.ForeignKey(
        Class, on_delete=models.CASCADE, null=True, blank=True
    )

    objects = StudentManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    objects = TeacherManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
