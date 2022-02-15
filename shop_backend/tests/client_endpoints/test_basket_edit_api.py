import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_basket_edit_by_anonymous(api_client, order_factory, product_factory):
    basket = order_factory()
    product = product_factory(make_m2m=True)
    payload = {'positions': [
        {
            'id': product.infos.first().id,
            'quantity': 10
        }
    ]
    }
    url = reverse('basket-detail', args=(basket.id,))
    response = api_client.put(url, data=payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_basket_edit_by_unconfirmed_client(api_client, user_factory, product_factory, order_factory):
    client = user_factory(is_confirmed=False)
    client_token = Token.objects.create(user=client)
    product = product_factory(make_m2m=True)
    payload = {'positions': [
        {
            'id': product.infos.first().id,
            'quantity': 10
        }
    ]
    }
    basket = order_factory(status='basket', user=client)
    url = reverse('basket-detail', args=(basket.id,))
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {client_token.key}')
    response = api_client.put(url, data=payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_basket_edit_by_supplier(api_client, user_factory, product_factory, order_factory):
    supplier = user_factory(is_confirmed=False)
    supplier_token = Token.objects.create(user=supplier)
    product = product_factory(make_m2m=True)
    payload = {'positions': [
        {
            'id': product.infos.first().id,
            'quantity': 10
        }
    ]
    }
    basket = order_factory(status='basket', user=supplier)
    url = reverse('basket-detail', args=(basket.id,))
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {supplier_token.key}')
    response = api_client.put(url, data=payload)
    assert response.status_code == 403
