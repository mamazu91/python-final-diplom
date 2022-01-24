import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_shops_states_list_by_anonymous(api_client, shop_factory):
    shop_factory(_quantity=2)
    url = reverse('shops_states-list')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_shops_states_list_by_client(api_client, user_factory, shop_factory):
    # Intention here is to create a client with already confirmed email,
    # as I am not really interested in testing its confirmation
    client = user_factory()
    client_token = Token.objects.create(user=client)

    shop_factory(_quantity=2)
    url = reverse('shops_states-list')
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {client_token.key}')
    response = api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_shops_states_list_by_supplier(api_client, user_factory, shop_factory):
    supplier = user_factory()
    supplier_token = Token.objects.create(user=supplier)
    supplier_shops = shop_factory(_quantity=2, user=supplier)

    # Intention here is to create a different set of shops
    # that would have a supplier different from the one declared in {supplier}
    shop_factory(_quantity=3)
    url = reverse('shops_states-list')
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {supplier_token.key}')
    response = api_client.get(url)
    assert response.status_code == 200
    assert sorted([shop.name for shop in supplier_shops]) == sorted([shop.get('name') for shop in response.data])

    # Intention here is to check that all the shops will have is_closed field,
    # because basically returning this field for the shops is kind of the main thing of this API.
    # Also had to create this sort of hack with sum() because 'is_closed' is bool,
    # meaning that all() would evaluate list of 'is_closed' differently depending on their values.
    assert sum([1 for shop in response.data if shop.get('is_closed') is False]) == len(supplier_shops)
