from django.db import models
from contacts.models import User
from products.models import ProductInfo


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_delivery', 'В доставке'),
        ('completed', 'Завершен')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders', verbose_name='Пользователь')
    parent_order_id = models.PositiveIntegerField(default=0, verbose_name='Внутренний идентификатор категории')
    positions = models.ManyToManyField(ProductInfo, through='OrderContent', verbose_name='Список продуктов')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Дата создания')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='basket', verbose_name='Состояние')
    delivery_address = models.CharField(max_length=255, default=None, verbose_name='Адрес доставки', blank=True,
                                        null=True)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders list'
        ordering = ['-created_at']


class OrderContent(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('shipped', 'Отправлена'),
        ('delivered', 'Доставлена')
    ]
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='contents',
                                     verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='contents', verbose_name='Заказ')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new', verbose_name='Состояние')

    class Meta:
        verbose_name = 'order content'
        verbose_name_plural = 'orders contents list'
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'order'], name='unique_order_item'),
        ]
