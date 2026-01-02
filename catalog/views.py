from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from .models import Product
from blog.models import BlogPost



class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        for product in context['products']:
            print(f"{product.name} - {product.created_at}")

        context['recent_posts'] = BlogPost.objects.filter(
            is_published=True
        ).order_by('-created_at')[:3]

        print(f"Продуктов: {context['products'].count()}")
        print(f"Постов: {context['recent_posts'].count()}")

        return context


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'  # вместо 'object'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context