from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Post, Category

menu = ['home', 'about', 'posts']
items = {
    'Smartphone': {
        'id': 1,
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    },
    'Laptop': {
        'id': 2,
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    },
    'Keyboard': {
        'id': 3,
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    },
    'Mouse': {
        'id': 4,
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    }
}


def home(request):
    data = {
        'menu_bar': menu,
        'products': items
    }
    return render(request, 'blog/index.html', context=data)


def product(request, product_id):
    product_lst = [i for i in items if items[i]['id'] == product_id]
    return render(request, 'blog/product.html',
                  {'product_desc': items[product_lst[0]], 'product_name': product_lst[0]})


def about(request):
    return render(request, 'blog/about.html')


def posts_list(request):
    posts = Post.objects.all()
    # print(posts)
    return render(request, 'blog/index.html', {'posts': posts})


def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # try:
    #     post = Post.objects.get(id=post_id)
    # except Post.DoesNotExist:
    #     raise Http404('Not found')
    # post = Post.objects.filter(id=post_id)
    # print(post)
    return render(request, 'blog/product.html', {'post': post})


def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/index.html', {'posts': posts})
