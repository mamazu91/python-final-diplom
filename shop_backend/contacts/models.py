from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def __create_user(self, email, password):
        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_supplier(self, email, password):
        user = self.__create_user(
            email,
            password=password
        )
        user.role = 'S'
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.__create_user(
            email,
            password=password
        )
        user.role = 'A'
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [('C', 'Клиент'), ('S', 'Поставщик'), ('A', 'Администратор')]
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    middle_name = models.CharField(max_length=50, verbose_name='Отчество')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    company = models.CharField(max_length=50, verbose_name='Компания')
    position = models.CharField(max_length=50, verbose_name='Позиция')
    role = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=8)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ['email']


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts', blank=True,
                             verbose_name='Пользователь')
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    house = models.CharField(max_length=10, blank=True, verbose_name='Дом')
    building = models.CharField(max_length=10, blank=True, verbose_name='Строение')
    structure = models.CharField(max_length=10, blank=True, verbose_name='Корпус')
    apartment = models.CharField(max_length=10, blank=True, verbose_name='Квартира')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = "Список контактов пользователей"
