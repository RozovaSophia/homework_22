from django import forms
from django.core.exceptions import ValidationError
from .models import Product
from .constants import FORBIDDEN_WORDS


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

    def __init__(self, *args, **kwargs):
        """Добавляем стилизацию полям формы"""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'margin-bottom: 15px;'
            })

        self.fields['name'].widget.attrs.update({
            'placeholder': 'Введите название продукта',
            'class': 'form-control form-control-lg'
        })

        self.fields['description'].widget.attrs.update({
            'placeholder': 'Введите описание продукта',
            'rows': 4,
            'class': 'form-control'
        })

        self.fields['price'].widget.attrs.update({
            'placeholder': '0.00',
            'min': '0',
            'step': '0.01',
            'class': 'form-control'
        })

        self.fields['image'].widget.attrs.update({
            'class': 'form-control-file'
        })

    def clean_name(self):
        """Валидация названия на запрещённые слова"""
        name = self.cleaned_data.get('name', '').lower()

        for forbidden_word in FORBIDDEN_WORDS:
            if forbidden_word in name:
                raise ValidationError(
                    f'Название содержит запрещённое слово: "{forbidden_word}"'
                )

        return self.cleaned_data['name']

    def clean_description(self):
        """Валидация описания на запрещённые слова"""
        description = self.cleaned_data.get('description', '').lower()

        for forbidden_word in FORBIDDEN_WORDS:
            if forbidden_word in description:
                raise ValidationError(
                    f'Описание содержит запрещённое слово: "{forbidden_word}"'
                )

        return self.cleaned_data['description']

    def clean_price(self):
        """Валидация цены (не может быть отрицательной)"""
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной')

        return price

    def clean(self):
        """Общая валидация формы"""
        cleaned_data = super().clean()

        # Дополнительная проверка: нельзя использовать цифры в качестве названия
        name = cleaned_data.get('name', '')
        if name.isdigit():
            raise ValidationError({
                'name': 'Название не может состоять только из цифр'
            })

        return cleaned_data