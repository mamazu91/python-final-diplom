# Работа с API
## Создание поставщика
Изначально приложение не имеет в базе ни клиентов, ни поставщиков. Простейший способ создать поставщика - с помощью Django shell:
```python
python manage.py shell
from contacts.models import User
User.objects.create_supplier(email='supplier@gmail.com', password='password')
```
**email** и **password** - обязательные параметры. При регистрации поставщика письмо с подтверждением имейла **не** отправляется.

## Создание пользователя
Создание пользователя происходит через отправку **POST** запроса на API **/api/v1/reg/**. Пример тела запроса:
```python
{
    "first_name": "Maksim",
    "middle_name": "Andreevich",
    "last_name": "Ksenofontov",
    "email": "mamazu91@gmail.com",
    "password": "password",
    "password_repeat": "password",
    "company": "Freelancer",
    "position": "Python Developer"
}
```
Все указанные параметры являются обязательными. После регистрации пользователя на указанный имейл приходит письмо с токеном для его подтверждения.

## Подтверждение имейла пользователя
Для подтверждения имейла необходимо отправить **POST** запрос с полученным токеном на API **/api/v1/confirm/**. Пример тела запроса:
```python
{
    "token": "a5cb2f336392b5d286d51babc8011b189824c09c"
}
```
Только после подтверждения пользователь получает возможность работы с пользовательскими API.


## Авторизация
