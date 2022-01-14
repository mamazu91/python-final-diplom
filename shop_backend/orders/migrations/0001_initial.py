# Generated by Django 3.2.9 on 2022-01-14 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0007_alter_product_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_order_id', models.PositiveIntegerField(default=0, verbose_name='Внутренний идентификатор категории')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('status', models.CharField(choices=[('assembled', 'Собран'), ('basket', 'Статус корзины'), ('canceled', 'Отменен'), ('confirmed', 'Подтвержден'), ('delivered', 'Доставлен'), ('new', 'Новый'), ('sent', 'Отправлен')], default='basket', max_length=15, verbose_name='Состояние')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Список заказов',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('status', models.CharField(choices=[('assembled', 'Собрана'), ('canceled', 'Отменена'), ('confirmed', 'Подтверждена'), ('delivered', 'Доставлена'), ('new', 'Новая'), ('sent', 'Отправлена')], default='new', max_length=15, verbose_name='Состояние')),
                ('order', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='orders.order', verbose_name='Заказ')),
                ('product_info', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='products.productinfo', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Содержимое заказа',
                'verbose_name_plural': 'Содержимое заказа',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='positions',
            field=models.ManyToManyField(blank=True, through='orders.OrderContent', to='products.ProductInfo', verbose_name='Список продуктов'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='ordercontent',
            constraint=models.UniqueConstraint(fields=('product_info', 'order'), name='unique_order_item'),
        ),
    ]
