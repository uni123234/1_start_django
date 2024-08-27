from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('home/', views.home, name="home"),
    path('items/<int:items_id>/',views.items , name="items"),
    path('about/', views.about, name="about"),
]