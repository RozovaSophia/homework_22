from django.shortcuts import render
from .models import Product


def home(request):

    latest_products = Product.objects.order_by('-created_at')[:5]


    for product in latest_products:
        print(f"{product.name} - {product.created_at}")

    context = {
        'title': 'Главная страница',
        'latest_products': latest_products,
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'catalog/contacts.html', context)