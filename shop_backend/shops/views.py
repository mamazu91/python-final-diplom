from rest_framework.viewsets import ModelViewSet
from .models import Shop
from .serializers import ShopSerializer, ShopImportSerializer, ShopStateSerializer
from orders.serializers import OrderSerializer
from .permissions import IsAuthenticatedSupplier
from rest_framework.response import Response


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
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


class OpenShopViewSet(ModelViewSet):
    queryset = Shop.objects.filter(is_closed=False)
    serializer_class = ShopSerializer
    http_method_names = ['get']
