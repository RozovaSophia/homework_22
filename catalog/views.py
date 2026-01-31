from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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
from .services import get_products_by_category
from django.core.cache import cache


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        context["recent_posts"] = BlogPost.objects.filter(is_published=True).order_by(
            "-created_at"
        )[:3]
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
    context_object_name = "product"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_cache_key(self):
        """Генерирует уникальный ключ кеша"""
        page = self.request.GET.get('page', 1)
        category = self.request.GET.get('category', 'all')
        sort = self.request.GET.get('sort', 'default')

        return f'product_list_page_{page}_cat_{category}_sort_{sort}'

    def get_queryset(self):
        cache_key = self.get_cache_key()

        # Проверяем кеш
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            print(f"✅ Загружено из кеша: {cache_key}")
            return cached_data

        # Запрос к БД
        queryset = Product.objects.filter(is_active=True)

        # Применяем фильтры из запроса
        category_id = self.request.GET.get('category')
        if category_id and category_id != 'all':
            queryset = queryset.filter(category_id=category_id)

        # Применяем сортировку
        sort_by = self.request.GET.get('sort')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('name')

        # Сохраняем в кеш на 5 минут
        cache.set(cache_key, queryset, 300)
        print(f"💾 Сохранено в кеш: {cache_key}")

        return queryset


class ProductCreateView(CreateView):
    login_url = "/users/login/"
    redirect_field_name = "next"
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        from .constants import FORBIDDEN_WORDS
        context = super().get_context_data(**kwargs)
        context["forbidden_words"] = FORBIDDEN_WORDS
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        from .constants import FORBIDDEN_WORDS
        context = super().get_context_data(**kwargs)
        context["forbidden_words"] = FORBIDDEN_WORDS
        return context

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")

    @method_decorator(cache_page(300))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.owner or user.has_perm('catalog.delete_product')


@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_published = False

        product.save()
        return redirect('catalog:product_detail', pk=pk)

    return render(request, 'catalog/unpublish_confirm.html', {'product': product})


def products_by_category_view(request, category_id):
    """Представление для отображения продуктов по категории"""
    category = get_object_or_404(Category, id=category_id)

    products = get_products_by_category(category_id)

    context = {
        'category': category,
        'products': products,
        'title': f'Продукты категории: {category.name}',
        'products_count': len(products),
    }

    return render(request, 'catalog/products_by_category.html', context)