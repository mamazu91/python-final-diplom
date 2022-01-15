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
Создание пользователя происходит через отправку **POST** запроса на API **/api/v1/reg/**. Пример запроса:
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
Для подтверждения имейла необходимо отправить **POST** запрос с полученным токеном на API **/api/v1/confirm/**. Пример запроса:
```python
{
    "token": "a5cb2f336392b5d286d51babc8011b189824c09c"
}
```
При прохождении процедуры указанный токен обнуляется; пользователь получает возможность авторизации и работы с пользовательскими API.

## Авторизация
Для прохождения процедуры авторизации отправьте **POST** запроси на API . Пример тела запроса:
{
    "username": "mamazu91@gmail.com",
    "password": "password"
}

Заголовок должен содержать соответствующий токен. Пример:
```python
Authorization
Token ffb61b74e42a3e394830dff2702392b2393e6de9
```

