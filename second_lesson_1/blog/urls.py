from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('about/', views.about, name='about'),
    path('posts/', views.posts_list, name='posts'),
    path('posts/<int:post_id>/', views.post_details, name='post_details'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts')
]
