# Требования
- python >= 3.10
- django
- pytz
- psycopg2-binary
- djangorestframework
- requests
- pyyaml
- django-filter

# Установка
1. Скачать проект
2. Установить зависимости:
```bash
pip install -r requirements.txt
```
4. Создать базу:
```postgres
create database netology_final_diploma;
```
5. Сменить директорию на shop_backend
6. Запустить миграции:
```bash
python manage.py migrate
```
8. Создать поставщика:
```python
json manage.py shell
from contacts.models import User
User.objects.create_supplier(email='supplier@gmail.com', password='password')
```
