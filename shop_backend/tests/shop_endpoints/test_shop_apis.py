import pytest
from django.urls import reverse
from random import randrange


@pytest.mark.django_db
def test_open_shops_list(client, shop_factory):
    # Creating a closed shop
    shop_factory(is_closed=True)
    open_shops = shop_factory(_quantity=2)
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

    # Intention here is to create a product in a closed shop
    product_factory(shops__is_closed=True, make_m2m=True)

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
    assert product.name == response.data.get('name')

    # Intention here is to check that the product will have position_id in every shop it is available in,
    # because basically position_id is kind of the main thing of the whole application
    assert all(position.get('position_id') for position in response.data.get('available_in'))


@pytest.mark.django_db
def test_products_filter_category(client, category_factory, product_factory):
    # Intention here is to create a few products all of which would be in the same category
    category = category_factory(make_m2m=True)
    products = product_factory(_quantity=2, category__id=category, make_m2m=True)

    # Intention here is to create a different set of products all of which would be in a different category
    product_factory(_quantity=3, make_m2m=True)

    url = reverse('products-list')
    params = {'category': category.id}
    response = client.get(url, params)
    assert response.status_code == 200
    assert sorted([product.name for product in products]) == sorted(
        [product.get('name') for product in response.data])


@pytest.mark.django_db
def test_products_filter_category(client, shop_factory, product_factory):
    # Intention here is to create a few products all of which would be in the same set of shops
    shops = shop_factory(_quantity=3)
    products = product_factory(_quantity=2, shops=shops, make_m2m=True)

    # Intention here is to create a different set of products all of which would be in a different set of shops
    product_factory(_quantity=3, make_m2m=True)

    # 'random_shop' seems a bit cleaner than 'shops[randrange(0, len(shops))].id' in {params}, so defining it like this
    random_shop = shops[randrange(0, len(shops))].id

    url = reverse('products-list')
    params = {'shop': random_shop}
    response = client.get(url, params)
    assert response.status_code == 200
    assert sorted([product.name for product in products]) == sorted(
        [product.get('name') for product in response.data])
