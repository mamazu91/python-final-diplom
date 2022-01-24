import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token
import random
import string


@pytest.mark.django_db
def test_shop_import_by_anonymous(api_client):
    payload = {'filename': 'shop.yaml'}
    url = reverse('shop_import-list')
    response = api_client.post(url, data=payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_shop_import_by_client(api_client, user_factory):
    # Intention here is to create a client with already confirmed email,
    # as I am not really interested in testing its confirmation
    client = user_factory(is_confirmed=True)
    client_token = Token.objects.create(user=client)

    payload = {'filename': 'shop.yaml'}
    url = reverse('shop_import-list')
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {client_token.key}')
    response = api_client.post(url, data=payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_shop_import_by_supplier_wo_payload(api_client, user_factory):
    supplier = user_factory(is_supplier=True, is_confirmed=True)
    supplier_token = Token.objects.create(user=supplier)
    url = reverse('shop_import-list')
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {supplier_token.key}')
    response = api_client.post(url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_shop_import_by_supplier_non_existing_file(api_client, user_factory):
    supplier = user_factory(is_supplier=True, is_confirmed=True)
    supplier_token = Token.objects.create(user=supplier)

    # Intent here is to pass a string with random numbers and characters to avoid situations when the test would become
    # successful should someone decide to create a file with name that would have been predefined here.
    payload = {'filename': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}
    url = reverse('shop_import-list')
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {supplier_token.key}')
    response = api_client.post(url, data=payload)
    assert response.status_code == 400
