from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.viewsets import ModelViewSet
from .serializers import BasketSerializer, UserOrderSerializer
from .permissions import IsAuthenticatedClient
from .models import Order
from django.http import HttpResponseNotFound
from shops.permissions import IsAuthenticatedSupplier
from django.db.models import Q
from rest_framework.response import Response


@extend_schema_view(
    list=extend_schema(
        summary="Get basket content",
        description='Get list of products positions in your basket, including their total.',
    ),
    retrieve=extend_schema(exclude=True),
    update=extend_schema(
        summary="Add products positions to basket",
        description="Add products positions to basket "
                    "by providing id uniquely identifying your basket. "
                    "Specifying more positions than there is in stock is going to cause an error. "
                    "Product position is relation between specific shop and one of its product, "
                    "which can be obtained via endpoint api/v1/products/",
    ),
    partial_update=extend_schema(
        summary="Empty basket",
        description='Empty basket of specific client '
                    'by providing id uniquely identifying the client.',
    )
)
@extend_schema(
    responses={
        200: OpenApiResponse(response=BasketSerializer),
        401: OpenApiResponse(description='Unauthorized'),
        403: OpenApiResponse(description='Forbidden')
    }
)
class BasketViewSet(ModelViewSet):
    """
    ModelViewSet for retrieving, emptying and modifying clients baskets.
    Endpoint: /api/v1/basket/
    """
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticatedClient]
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='basket')

    def retrieve(self, request, *args, **kwargs):
        return HttpResponseNotFound

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = super().get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if partial:
            instance.contents.all().delete()
        else:
            self.perform_update(serializer)

        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary='Get list of orders',
        description='Get list of your both open and closed orders.',
        responses={
            200: OpenApiResponse(response=UserOrderSerializer),
            401: OpenApiResponse(description='Unauthorized'),
            403: OpenApiResponse(description='Forbidden')
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
            401: OpenApiResponse(description='Unauthorized'),
            403: OpenApiResponse(description='Forbidden')
        }
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
