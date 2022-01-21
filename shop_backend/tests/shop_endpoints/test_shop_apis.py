import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_open_shops_list(client, shop_factory):
    open_shops = shop_factory(_quantity=2)
    shop_factory(is_closed=True)  # Creating a closed shop

    url = reverse('open_shops-list')
    response = client.get(url)
    assert response.status_code == 200
    assert sorted([shop.name for shop in open_shops]) == sorted([shop.get('name') for shop in response.data])


@pytest.mark.django_db
def test_categories_list(client, category_factory):
    categories = category_factory(_quantity=2, make_m2m=True)

    url = reverse('categories-list')
    response = client.get(url)
    assert response.status_code == 200
    assert sorted([category.name for category in categories]) == sorted(
        [category.get('name') for category in response.data])


@pytest.mark.django_db
def test_products_list(client, product_factory):
    open_shop_products = product_factory(_quantity=2, make_m2m=True)
    product_factory(shops__is_closed=True, make_m2m=True)  # Creating a closed shop here

    url = reverse('products-list')
    response = client.get(url)
    assert response.status_code == 200
    assert sorted([product.name for product in open_shop_products]) == sorted(
        [product.get('name') for product in response.data])


@pytest.mark.django_db
def test_products_detail(client, product_factory):
    product = product_factory(make_m2m=True)
    url = reverse('products-detail', args=(product.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'position_id' in response.data.get('available_in')
