from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer


@extend_schema_view(
    retrieve=extend_schema(description='Get product category.'),
    list=extend_schema(description='Get list of products categories.')
)
class CategoryViewSet(ModelViewSet):
    """
    ModelViewSet for retrieving and listing products categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get']
