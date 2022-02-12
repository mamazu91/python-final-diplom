from django.db import models
from shops.models import Shop


class Category(models.Model):
    shops = models.ManyToManyField(Shop, through='ShopCategory', related_name='categories',
                                   verbose_name='Список магазинов')
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories list'
        ordering = ['-name']


class ShopCategory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    internal_category_id = models.PositiveIntegerField(verbose_name='Внутренний идентификатор категории')

    class Meta:
        verbose_name = 'shop category'
        verbose_name_plural = 'shops categories list'
        constraints = [models.UniqueConstraint(fields=['shop', 'category'], name='unique_shop_category')]
