from django.shortcuts import render
from .models import Menu


def index(request):
    first_menu_item = Menu.objects.filter(parent=None).first()
    context = {}
    if first_menu_item:
        context['slug'] = first_menu_item.slug
    return render(request, 'index.html', context)


def item(request, slug):
    return render(request, 'index.html', {'slug': slug})
