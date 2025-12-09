from django.shortcuts import render

def home(request):
    """Контроллер для домашней страницы"""
    return render(request, 'catalog/home.html')

def contacts(request):
    """Контроллер для страницы контактов"""
    return render(request, 'catalog/contacts.html')