from django.core.cache import cache
from .models import Product


def get_products_by_category(category_id, use_cache=True):
    """
    Возвращает список продуктов по категории
    Использует кеширование если use_cache=True
    """
    cache_key = f'products_category_{category_id}'

    if use_cache:
        products = cache.get(cache_key)
        if products is not None:
            print(f"Продукты категории {category_id} загружены из кеша")
            return products

    products = list(Product.objects.filter(
        category_id=category_id,
        is_active=True
    ).select_related('category', 'owner'))

    if use_cache:
        cache.set(cache_key, products, 600)
        print(f"Продукты категории {category_id} загружены из БД и сохранены в кеш")

    return products


def get_all_products(use_cache=True):
    """
    Возвращает все активные продукты с кешированием
    """
    cache_key = 'all_active_products'

    if use_cache:
        products = cache.get(cache_key)
        if products is not None:
            print("Все продукты загружены из кеша")
            return products

    products = list(Product.objects.filter(
        is_active=True
    ).select_related('category', 'owner').prefetch_related('tags'))

    if use_cache:
        cache.set(cache_key, products, 600)
        print("Все продукты загружены из БД и сохранены в кеш")

    return products


def clear_product_cache():
    """Очищает все кеши продуктов"""
    cache_keys = [
        'all_active_products',
    ]

    from django.core.cache import cache
    cache.delete_many(cache_keys)

    print("Кеш продуктов очищен")