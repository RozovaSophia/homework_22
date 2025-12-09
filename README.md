# Django Catalog Project

## Описание проекта
Этот проект представляет собой веб-приложение на Django с каталогом товаров.

## Установка и запуск

1. **Клонируйте репозиторий:**

git clone <ваш-репозиторий>
Создайте виртуальное окружение:

python -m venv .venv
2. Активируйте виртуальное окружение:

Windows: .venv\Scripts\activate

Linux/Mac: source .venv/bin/activate

3. Установите зависимости:

pip install django

или, если есть файл requirements.txt:

pip install -r requirements.txt

4. Примените миграции:

python manage.py migrate

5. Запустите сервер:

python manage.py runserver