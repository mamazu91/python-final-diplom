from rest_framework.viewsets import ModelViewSet
from .models import Order
from .serializers import BasketSerializer, UserOrderSerializer
from contacts.permissions import IsAuthenticatedClient
from shops.permissions import IsAuthenticatedSupplier
from django.db.models import Q
from rest_framework.response import Response


class BasketViewSet(ModelViewSet):
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticatedClient]
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='basket')

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


class UserOrderViewSet(ModelViewSet):
    serializer_class = UserOrderSerializer
    permission_classes = [IsAuthenticatedClient | IsAuthenticatedSupplier]
    http_method_names = ['post', 'get', 'patch']

    def get_queryset(self):
        return Order.objects.filter(~Q(status='basket'), user=self.request.user)
