from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer


@extend_schema_view(
    retrieve=extend_schema(
        summary='Get product category',
        description='Get specific product category '
                    'by providing id uniquely identifying the category.',
        responses={
            200: OpenApiResponse(response=CategorySerializer),
            404: OpenApiResponse(description='Category with this id was not found')
        },
        tags=['common']
    ),
    list=extend_schema(
        summary='Get list of products categories',
        description='Get list of all unique products categories from all existing shops.',
        tags=['common']
    )
)
class CategoryViewSet(ModelViewSet):
    """
    ModelViewSet for retrieving and listing products categories.
    Endpoint: /api/v1/categories/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get']
