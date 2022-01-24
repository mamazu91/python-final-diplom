import pytest
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def shop_factory():
    def factory(**kwargs):
        return baker.make('shops.Shop', **kwargs)

    return factory


@pytest.fixture()
def category_factory():
    def factory(**kwargs):
        return baker.make('categories.Category', **kwargs)

    return factory


@pytest.fixture()
def product_factory():
    def factory(**kwargs):
        return baker.make('products.Product', **kwargs)

    return factory


@pytest.fixture()
def user_factory():
    def factory(**kwargs):
        return baker.make('contacts.User', **kwargs)

    return factory
