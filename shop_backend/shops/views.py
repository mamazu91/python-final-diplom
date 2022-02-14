from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.viewsets import ModelViewSet
from .models import Shop
from .serializers import BaseShopSerializer, ShopImportSerializer, ShopStateSerializer
from .permissions import IsAuthenticatedSupplier
from rest_framework.response import Response


@extend_schema(
    summary="Import shop-related data from a yaml file",
    description='File must at least contain information on shop, its categories, and their goods.',
    request={'application/json': ShopImportSerializer},
    responses={
        201: OpenApiResponse(response=ShopImportSerializer),
        400: OpenApiResponse(description='Bad Request'),
        401: OpenApiResponse(description='Unauthorized'),
        403: OpenApiResponse(description='Forbidden')
    },
)
class ShopImportViewSet(ModelViewSet):
    """
    ModelViewSet for importing shops-related data from yaml files.
    Endpoint: /api/v1/partner/import/
    """
    queryset = Shop.objects.all()
    serializer_class = ShopImportSerializer
    permission_classes = [IsAuthenticatedSupplier]
    http_method_names = ['post']


@extend_schema_view(
    retrieve=extend_schema(
        summary='Get shop state',
        description='Get state of specific shop '
                    'by providing id uniquely identifying the shop.',
    ),
    list=extend_schema(
        summary='Get list of shops states',
        description='Get list of states of all shops associated with your account.',
    ),
    update=extend_schema(
        summary='Change shop state',
        description='Change state of specific shop '
                    'by providing id uniquely identifying the shop.',
        request={'application/json': ShopStateSerializer},
        responses={
            200: OpenApiResponse(response=ShopStateSerializer),
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(description='Unauthorized'),
            403: OpenApiResponse(description='Forbidden')
        },
    ),
)
class ShopStateViewSet(ModelViewSet):
    """
    ModelViewSet for retrieving, listing and modifying shops states (from closed to open, or vice versa).
    Endpoint: /api/v1/partner/states/
    """
    serializer_class = ShopStateSerializer
    permission_classes = [IsAuthenticatedSupplier]
    http_method_names = ['get', 'put']

    def get_queryset(self):
        return Shop.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'results': 'There is no shops associated with your account.'})

        serializer = super().get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema_view(
    retrieve=extend_schema(
        summary='Get open shop',
        description='Get specific open shop '
                    'by providing id uniquely identifying the shop.',
        tags=['common']
    ),
    list=extend_schema(
        summary='Get list of open shops',
        description='Get list of all existing and open shops.',
        tags=['common']
    )
)
class OpenShopViewSet(ModelViewSet):
    """
    ModelViewSet for retrieving and listing open shops.
    Endpoint: /api/v1/shop/shops/
    """
    queryset = Shop.objects.filter(is_closed=False)
    serializer_class = BaseShopSerializer
    http_method_names = ['get']
