from django.shortcuts import render
menu = ['home','about','post']
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
    menu = ["home", "about", "posts"]

    data = {
        'menu': menu,
        'items': items
    }
    return render(request,'blog/index.html', context=data)


def about(request):
    return render(request, 'blog/about.html')


def items(request,items_id):
    items = [i for i in items if items[i]['id'] == items_id]
    return render(request, 'blog/items.html', {'items_description': items[items_lst[0]], 'items_name': items_lst[0]})