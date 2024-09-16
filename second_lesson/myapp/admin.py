from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Student, Teacher, School, Class, CustomUser, Subject


class AlphabeticalOrderFilter(admin.SimpleListFilter):
    title = "Sort by Name"
    parameter_name = "alphabetical_order"

    def lookups(self, request, model_admin):
        return [
            ("asc", "A-Z"),
            ("desc", "Z-A"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "asc":
            return queryset.order_by("first_name")
        if self.value() == "desc":
            return queryset.order_by("-first_name")


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_teacher",
        "is_student",
    ]
    list_filter = [
        "is_active",
        "is_staff",
        "is_teacher",
        "is_student",
        "date_joined",
        AlphabeticalOrderFilter,
    ]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Information", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_teacher",
                    "is_student",
                    "is_superuser",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    def get_ordering(self, request):
        """Сортування за електронною поштою та датою приєднання за замовчуванням."""
        return ["email", "date_joined"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "school", "class_number", "age"]
    search_fields = ["first_name", "last_name", "school__name"]
    list_filter = ["school", "class_number", "age", "gender", AlphabeticalOrderFilter]
    ordering = ["last_name"]

    def get_ordering(self, request):
        return ["last_name"]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "school", "subject"]
    search_fields = ["first_name", "last_name", "school__name", "subject__name"]
    list_filter = [
        "school",
        "subject",
        "years_of_experience",
        "gender",
        AlphabeticalOrderFilter,
    ]
    ordering = ["last_name"]


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ["name", "school_number", "address", "type_of_school"]
    search_fields = ["name", "school_number", "address"]
    list_filter = ["type_of_school", "city", AlphabeticalOrderFilter]
    ordering = ["name"]


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ["class_number", "school", "location", "class_teacher"]
    search_fields = ["class_number", "school__name", "location"]
    list_filter = ["school", "class_number", "location", AlphabeticalOrderFilter]
    ordering = ["class_number"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "school"]
    search_fields = ["name", "code", "school__name"]
    list_filter = ["school", "code", AlphabeticalOrderFilter]
    ordering = ["name"]
