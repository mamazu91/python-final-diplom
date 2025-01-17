# Generated by Django 4.0.1 on 2022-01-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
        ('categories', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='shops',
            field=models.ManyToManyField(related_name='categories', through='categories.ShopCategory', to='shops.Shop', verbose_name='Список магазинов'),
        ),
    ]
