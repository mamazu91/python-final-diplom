import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_shop_state_change_by_anonymous(api_client, shop_factory):
    shop = shop_factory()
    payload = {'is_closed': 'True'}
    url = reverse('shops_states-detail', args=(shop.id,))
    response = api_client.put(url, data=payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_shop_state_change_by_client(api_client, user_factory, shop_factory):
    # Intention here is to create a client with already confirmed email,
    # as I am not really interested in testing its confirmation
    client = user_factory(is_confirmed=True)
    client_token = Token.objects.create(user=client)

    shop = shop_factory()
    payload = {'is_closed': 'True'}
    url = reverse('shops_states-detail', args=(shop.id,))
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {client_token.key}')
    response = api_client.put(url, data=payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_shop_state_change_by_supplier_wo_payload(api_client, user_factory, shop_factory):
    # Intention here is to create a client with already confirmed email,
    # as I am not really interested in testing its confirmation
    supplier = user_factory(is_supplier=True, is_confirmed=True)
    supplier_token = Token.objects.create(user=supplier)
    shop = shop_factory(user=supplier)

    url = reverse('shops_states-detail', args=(shop.id,))
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {supplier_token.key}')
    response = api_client.put(url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_shop_state_change_by_supplier_w_payload(api_client, user_factory, shop_factory):
    # Intention here is to create a client with already confirmed email,
    # as I am not really interested in testing its confirmation
    supplier = user_factory(is_supplier=True, is_confirmed=True)
    supplier_token = Token.objects.create(user=supplier)
    shop = shop_factory(user=supplier)

    payload = {'is_closed': True}
    url = reverse('shops_states-detail', args=(shop.id,))
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {supplier_token.key}')
    response = api_client.put(url, data=payload)
    assert response.status_code == 200
    assert shop.name == response.data.get('name')
    assert payload.get('is_closed') == response.data.get('is_closed')
