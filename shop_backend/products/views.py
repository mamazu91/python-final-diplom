from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductDetailsSerializer, ProductSerializer
from .models import Product
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductShopCategoryFilter
from rest_framework.response import Response


@extend_schema_view(
    retrieve=extend_schema(
        summary="Get product and details on its availability in shops",
        description="Get specific product by providing id uniquely identifying this product. "
                    "Also returns list of all necessary details about the product's availability in shops.",
        responses={
            200: OpenApiResponse(response=ProductDetailsSerializer),
            404: OpenApiResponse(description='Product with this id was not found')
        },
        tags=['common']
    ),
    list=extend_schema(
        summary='Get list of products in all shops',
        description='Get list of all products from all open shops. Can be filtered by category_id or/and shop_id.',
        tags=['common']
    )
)
class ProductViewSet(ModelViewSet):
    """
    ModelViewSet for retrieving and listing products.
    Endpoint: /api/v1/products/
    """
    queryset = Product.objects.filter(shops__is_closed=False).distinct('name')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductShopCategoryFilter
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        """
        Method for retrieving product and details on its availability in shops.
        """
        instance = super().get_object()
        serializer = ProductDetailsSerializer(instance)
        return Response(serializer.data)
