import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_basket_get_by_anonymous(api_client, order_factory):
    order_factory(status='basket')
    url = reverse('basket-list')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_basket_get_by_unconfirmed_client(api_client, user_factory, order_factory):
    client = user_factory(is_confirmed=False)
    client_token = Token.objects.create(user=client)
    order_factory(status='basket', user=client)
    url = reverse('basket-list')
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {client_token.key}')
    response = api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_basket_get_by_supplier(api_client, user_factory, order_factory):
    supplier = user_factory(is_supplier=True, is_confirmed=True)
    supplier_token = Token.objects.create(user=supplier)
    order_factory(status='basket', user=supplier)
    url = reverse('basket-list')
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {supplier_token.key}')
    response = api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_basket_get_by_client(api_client, user_factory, order_factory):
    # Intention here is to create a client with already confirmed email,
    # as I am not really interested in testing its confirmation
    client = user_factory(is_confirmed=True)
    client_token = Token.objects.create(user=client)
    order_factory(status='basket', user=client)
    url = reverse('basket-list')
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {client_token.key}')
    response = api_client.get(url)
    assert response.status_code == 200

    # Intention here is to check that only 3 fields: 'id', 'total' and 'positions'
    # are going to be returned by the basket API
    assert [data for position in response.data for data in position.keys()] == ['id', 'total', 'positions']
