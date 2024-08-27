from django.shortcuts import render


def homes(request):
    menu_bar = ["abama"]

    data = {
        'menu_bar': menu_bar
    }
    return render(request,'blog/index.html', context=data)


def abouts(request):
    return render(request, 'blog/about.html')