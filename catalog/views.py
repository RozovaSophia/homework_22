from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from blog.models import BlogPost
from .models import Product, Category
from .forms import ProductForm


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"

        for product in context["products"]:
            print(f"{product.name} - {product.created_at}")

        context["recent_posts"] = BlogPost.objects.filter(is_published=True).order_by(
            "-created_at"
        )[:3]

        print(f"Продуктов: {context['products'].count()}")
        print(f"Постов: {context['recent_posts'].count()}")

        return context


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Контакты"
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"  # вместо 'object'
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context


class ProductListView(ListView):
    """Список всех продуктов"""

    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12


class ProductCreateView(CreateView):
    """Создание продукта"""

    login_url = "/users/login/"
    redirect_field_name = "next"
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("product_list")

    def get_context_data(self, **kwargs):
        from .constants import FORBIDDEN_WORDS

        context = super().get_context_data(**kwargs)
        context["forbidden_words"] = FORBIDDEN_WORDS
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        from .constants import FORBIDDEN_WORDS

        context = super().get_context_data(**kwargs)
        context["forbidden_words"] = FORBIDDEN_WORDS
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта"""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")
