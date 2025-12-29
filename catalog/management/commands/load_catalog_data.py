import os
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Загружает фикстуры для каталога (удаляет старые данные)'

    def handle(self, *args, **options):
        from catalog.models import Product, Category
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Старые данные удалены')


        fixtures_dir = os.path.join('catalog', 'fixtures')

        call_command('loaddata', os.path.join(fixtures_dir, 'categories.json'))
        self.stdout.write('Категории загружены')

        call_command('loaddata', os.path.join(fixtures_dir, 'products.json'))
        self.stdout.write('Продукты загружены')

        self.stdout.write(self.style.SUCCESS('Все данные успешно загружены!'))