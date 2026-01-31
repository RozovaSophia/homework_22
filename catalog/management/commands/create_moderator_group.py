from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" с необходимыми правами'

    def handle(self, *args, **kwargs):
        # Создаем или получаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        # Получаем разрешения
        content_type = ContentType.objects.get_for_model(Product)

        # 1. Кастомное право на отмену публикации
        unpublish_perm, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            content_type=content_type,
            defaults={'name': 'Может отменять публикацию продукта'}
        )

        # 2. Право на удаление любого продукта
        delete_perm = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )

        # Добавляем права группе
        group.permissions.add(unpublish_perm, delete_perm)

        self.stdout.write(self.style.SUCCESS(
            f'Добавлено {group.permissions.count()} прав для группы "{group.name}"'
        ))