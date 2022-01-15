# Работа с API поставщика
## Создание поставщика
Простейший способ создать поставщика - с помощью Django shell:
```python
python manage.py shell
from contacts.models import User
User.objects.create_supplier(email='supplier@gmail.com', password='password')
```
**email** и **password** - обязательные параметры.

При регистрации поставщика письмо с подтверждением имейла **не** отправляется.

## Авторизация
Авторизация подразумевает получение токена. Для получения токена отправьте отправьте **POST** запрос на API **/api/v1/auth/**. Обязательные параметры: **username**, **password**.

Пример тела запроса:
```python
{
    "username": "mamazu91@gmail.com",
    "password": "password"
}
```

```python
Пример ответа:
{
    "token": "ffb61b74e42a3e394830dff2702392b2393e6de9"
}
```

## Импорт товаров магазина из yaml файла
Для импорта товаров отправьте **POST** запрос на API **/api/v1/partner/import/** с указанием заголовкам, содержащего токен поставщика. Обязательные параметры: **filename** - абсолютный или относительный путь до файла с товарами на файловой системе.

Пример тела запроса:
```python
{
    "filename" : "shop1.yaml"
}
```

Пример заголовка:
```python
Authorization
Token ffb61b74e42a3e394830dff2702392b2393e6de9
```

```python
{
    "id": 1,
    "name": "Связной",
    "filename": "shop1.yaml"
}

# Работа с API клиента
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
