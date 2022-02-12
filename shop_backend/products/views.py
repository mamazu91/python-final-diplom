from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer, ProductDetailsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductShopCategoryFilter
from rest_framework.response import Response


@extend_schema_view(
    retrieve=extend_schema(summary="Get product plus its details (per shop it's available in)",
                           description="Get specific product by providing its unique id. "
                                       "Also returns list of all necessary details for the product "
                                       "per shop it's available in.",
                           responses={200: OpenApiResponse(response=ProductDetailsSerializer)}),
    list=extend_schema(summary='Get list of products in all shops',
                       description='Simply returns list of all products from all open shops. '
                                   'Products from shops with field is_closed equal to True'
                                   ' are not going to be displayed. '
                                   'Can be filtered by category_id or/and shop_id.')
)
class ProductViewSet(ModelViewSet):
    """
    ModelViewSet for retrieving and listing products.
    """
    queryset = Product.objects.filter(shops__is_closed=False).distinct('name')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductShopCategoryFilter
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        """
        Method for retrieving product plus its details per every shop it's available in.
        """
        instance = super().get_object()
        serializer = ProductDetailsSerializer(instance)
        return Response(serializer.data)
