from rest_framework.viewsets import ModelViewSet
from .models import Shop
from .serializers import BaseShopSerializer, ShopImportSerializer, ShopStateSerializer
from .permissions import IsAuthenticatedSupplier
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = BaseShopSerializer
    http_method_names = ['get']


class ShopImportViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopImportSerializer
    permission_classes = [IsAuthenticatedSupplier]
    http_method_names = ['post']


class ShopStateViewSet(ModelViewSet):
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
    retrieve=extend_schema(summary='Get open shop',
                           description='Get specific open shop by providing its unique id. '
                                       'Shops with field is_closed equal to True are not going to be displayed.'),
    list=extend_schema(summary='Get list of open shops',
                       description='Get list of open shops. '
                                   'Shops with field is_closed equal to True are not going to be displayed.')
)
class OpenShopViewSet(ModelViewSet):
    """
    ModelViewSet for retrieving and listing open shops.
    """
    queryset = Shop.objects.filter(is_closed=False)
    serializer_class = BaseShopSerializer
    http_method_names = ['get']
