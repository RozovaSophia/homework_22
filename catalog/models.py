from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование',
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='products/%Y/%m/%d/',
        verbose_name='Изображение',
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True,
        null=True,
        related_name='products'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
        validators=[MinValueValidator(0)],
        db_index = True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный',
        help_text='Отображается ли продукт на сайте'
    )

    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество на складе'
    )

    in_stock = models.BooleanField(
        default=False,
        verbose_name='В наличии',
        editable=False
    )

    def clean(self):
        """Валидация на уровне модели"""
        from django.core.exceptions import ValidationError

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа',
                           'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in forbidden_words:
            if word in self.name.lower():
                raise ValidationError(
                    {'name': f'Название содержит запрещённое слово: "{word}"'}
                )

        if self.description:
            for word in forbidden_words:
                if word in self.description.lower():
                    raise ValidationError(
                        {'description': f'Описание содержит запрещённое слово: "{word}"'}
                    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-is_active', '-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.name} - {self.price} руб."


