from django.db import models
from categories.models import Category
from shops.models import Shop


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Список категорий')
    shops = models.ManyToManyField(Shop, through='ProductInfo', verbose_name='Список магазинов')
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products list'
        ordering = ['name']


class ProductInfo(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products', verbose_name='Магазин')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='infos', verbose_name='Продукт')
    internal_product_id = models.PositiveIntegerField(verbose_name='Внутренний идентификатор категории')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')

    class Meta:
        verbose_name = 'product info'
        verbose_name_plural = 'products infos list'
        constraints = [models.UniqueConstraint(fields=['shop', 'product'], name='unique_product_info')]


class Parameter(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Имя')
    products = models.ManyToManyField(Product, through='ParameterValue', blank=True, verbose_name='Список продуктов')

    class Meta:
        verbose_name = 'parameter'
        verbose_name_plural = 'parameters list'
        ordering = ['-name']


class ParameterValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='parameters', blank=True,
                                verbose_name='Продукт')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='values', blank=True,
                                  verbose_name='Параметр')
    value = models.CharField(max_length=50, verbose_name='Значение')

    class Meta:
        verbose_name = 'product parameter'
        verbose_name_plural = 'products parameters list'
        constraints = [models.UniqueConstraint(fields=['product', 'parameter'], name='unique_product_parameter')]
