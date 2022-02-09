from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse
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
        description="Get content of the specified client's basket."),
    retrieve=extend_schema(exclude=True),
    update=extend_schema(description="Add products to the specified client's basket."),
    partial_update=extend_schema(description="Empty basket of the specified client.")
)
@extend_schema(responses={
    200: OpenApiResponse(response=BasketSerializer),
    401: OpenApiResponse(description='Unauthorized'),
    403: OpenApiResponse(description='Forbidden')
}
)
class BasketViewSet(ModelViewSet):
    """
    ModelViewSet for retrieving, emptying and modifying clients baskets.
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


class UserOrderViewSet(ModelViewSet):
    serializer_class = UserOrderSerializer
    permission_classes = [IsAuthenticatedClient | IsAuthenticatedSupplier]
    http_method_names = ['post', 'get', 'patch']

    def get_queryset(self):
        return Order.objects.filter(~Q(status='basket'), user=self.request.user)
