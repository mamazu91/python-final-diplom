# Generated by Django 4.0.1 on 2022-01-25 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_category_alter_product_shops'),
        ('orders', '0003_alter_ordercontent_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='positions',
            field=models.ManyToManyField(through='orders.OrderContent', to='products.ProductInfo', verbose_name='Список продуктов'),
        ),
    ]