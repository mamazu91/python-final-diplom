import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_orders_list_by_anonymous(api_client, order_factory):
    order_factory(_quantity=2, make_m2m=True)
    url = reverse('shop_orders-list')
    response = api_client.get(url)
    assert response.status_code == 401


# @pytest.mark.django_db
# def test_orders_list_by_client(api_client, user_factory, order_factory):
#     # Intention here is to create a client with already confirmed email,
#     # as I am not really interested in testing its confirmation
#     client = user_factory(is_confirmed=True)
#     client_token = Token.objects.create(user=client)
#
#     order_factory(_quantity=2, user=client, make_m2m=True, status='new')
#     url = reverse('shop_orders-list')
#     api_client.credentials(HTTP_AUTHORIZATION=f'Token {client_token.key}')
#     response = api_client.get(url)
#     print(response.data)
#     assert response.status_code == 200
#     assert int(response.data.get('total')) > 0
