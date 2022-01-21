import pytest
from shops.models import Shop
from rest_framework.test import APIClient
from django.urls import reverse
from categories.models import Category
from products.models import Product


@pytest.mark.django_db
def test_open_shops_list():
    open_shops = Shop.objects.bulk_create(
        [
            Shop(name='open_shop_1'),
            Shop(name='open_shop_2'),
        ]
    )
    closed_shop = Shop.objects.create(name='closed_shop', is_closed=True)

    client = APIClient()
    url = reverse('open_shops-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == len(open_shops)
    assert closed_shop.name not in (response.data[0].get('name') and response.data[1].get('name'))


@pytest.mark.django_db
def test_categories_list():
    categories = Category.objects.bulk_create(
        [
            Category(name='category_1'),
            Category(name='category_2')
        ]
    )

    client = APIClient()
    url = reverse('categories-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == len(categories)


@pytest.mark.django_db
def test_products_list():
    open_shop = Shop.objects.create(name='open_shop')
    closed_shop = Shop.objects.create(name='closed_shop', is_closed=True)
    category = Category.objects.create(name='category')
    open_shop_products = Product.objects.bulk_create(
        [
            Product(name='product_1', category=category),
            Product(name='product_2', category=category)
        ]
    )
    closed_shop_products = Product.objects.bulk_create(
        [
            Product(name='product_3', category=category),
            Product(name='product_4', category=category)
        ]
    )

    for product in open_shop_products:
        product.shops.add(open_shop)

    for product in closed_shop:
        product.shops.add(closed_shop)

    client = APIClient()
    url = reverse('products-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == len(open_shop_products)
