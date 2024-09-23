from django.urls import path, include, re_path

app_name = "auth_me"

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
