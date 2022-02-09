from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer


@extend_schema_view(
    retrieve=extend_schema(summary='Get product category',
                           description='Get specific product category by providing its unique id.'),
    list=extend_schema(summary='Get list of products categories',
                       description='Get list of products categories.')
)
class CategoryViewSet(ModelViewSet):
    """
    ModelViewSet for retrieving and listing products categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get']
