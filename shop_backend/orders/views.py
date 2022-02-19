from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse
from rest_framework.viewsets import ModelViewSet
from .serializers import ClientBasketSerializer, UserOrderSerializer
from .permissions import IsAuthenticatedClient
from .models import Order
from django.http import HttpResponseNotFound
from shops.permissions import IsAuthenticatedSupplier
from django.db.models import Q
from rest_framework.response import Response


@extend_schema_view(
    list=extend_schema(
        summary='Get basket content',
        description='Get list of products positions in your basket, including their total.',
    ),
    retrieve=extend_schema(exclude=True),
    update=extend_schema(
        summary='Add products positions to basket',
        description='Add products positions to your basket. '
                    'Specifying more positions than there is in stock is going to cause an error. '
                    'Product position is relation between specific shop and one of its products, '
                    'which can be obtained via endpoint api/v1/products/',
        parameters=(
                [
                    OpenApiParameter(
                        "id",
                        OpenApiTypes.INT,
                        OpenApiParameter.PATH,
                        exclude=True
                    )
                ]
        )
    ),
    partial_update=extend_schema(
        summary='Empty basket',
        description='Empty content of your basket.',
        request=None,
        parameters=(
                [
                    OpenApiParameter(
                        "id",
                        OpenApiTypes.INT,
                        OpenApiParameter.PATH,
                        exclude=True
                    )
                ]
        )
    )
)
@extend_schema(
    responses={
        200: OpenApiResponse(response=ClientBasketSerializer),
        401: OpenApiResponse(description='Header is missing authorization token'),
        403: OpenApiResponse(description='Your account does not have enough permissions for this action')
    }
)
class ClientBasketViewSet(ModelViewSet):
    """
    ModelViewSet for retrieving, emptying and modifying clients baskets.
    Endpoint: /api/v1/client/basket/
    """
    serializer_class = ClientBasketSerializer
    permission_classes = [IsAuthenticatedClient]
    http_method_names = ['get', 'put', 'patch']

    def get_object(self):
        return Order.objects.get(user=self.request.user, status='basket')

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='basket')

    def retrieve(self, request, *args, **kwargs):
        return HttpResponseNotFound

    def put(self, request):
        instance = self.get_object()
        serializer = super().get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request):
        instance = self.get_object()
        serializer = super().get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance.contents.all().delete()
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary='Get list of orders',
        description='Get list of your both open and closed orders.',
        responses={
            200: OpenApiResponse(response=UserOrderSerializer),
            401: OpenApiResponse(description='Header is authorization missing token'),
            403: OpenApiResponse(description='Your account does not have enough permissions for this action')
        }
    ),
    retrieve=extend_schema(exclude=True),
    create=extend_schema(
        summary='Create a new order',
        description='Creates a new order based on your basket content. '
                    'Also creates order for each supplier products of which were detected in your new order. '
                    'Then empties basket, and sends notification emails to both you and all the suppliers.',
        request={'application/json': UserOrderSerializer},
        responses={
            201: OpenApiResponse(response=UserOrderSerializer),
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(description='Header is missing authorization token'),
            403: OpenApiResponse(description='Your account does not have enough permissions for this action')
        },
        tags=['client']
    )
)
class UserOrderViewSet(ModelViewSet):
    """
    ModelViewSet for creating orders for clients, as well as listing orders of both clients and suppliers.
    Endpoint:
        Clients: /api/v1/orders/
        Supplier: /api/v1/partner/orders/
    """
    serializer_class = UserOrderSerializer
    permission_classes = [IsAuthenticatedClient | IsAuthenticatedSupplier]
    http_method_names = ['post', 'get']

    def get_queryset(self):
        return Order.objects.filter(~Q(status='basket'), user=self.request.user)
