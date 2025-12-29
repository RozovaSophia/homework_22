from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):

    products = Product.objects.all()


    for product in products:
        print(f"{product.name} - {product.created_at}")

    context = {
        'title': 'Главная страница',
        'products': products,
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'catalog/contacts.html', context)

def product_detail(request, pk):
    """
    Контроллер для отображения подробной информации о товаре
    Принимает pk (id товара) в URL.
    """
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': product.name,
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context)


