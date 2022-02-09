from rest_framework.viewsets import ModelViewSet
from contacts.models import User
from .serializers import UserRegisterSerializer, UserConfirmSerializer, UserPasswordSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.authtoken.models import Token
from contacts.permissions import IsAuthenticatedClient
from shops.permissions import IsAuthenticatedSupplier


class UserRegisterViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']


@extend_schema(summary="Confirm client's email",
               description="Confirm client's email by specifying the token "
                           "that was sent to the client's email upon registration.",
               request={'application/json': UserConfirmSerializer},
               responses={
                   201: OpenApiResponse(response=UserConfirmSerializer),
                   400: OpenApiResponse(description='Bad Request')
               }
               )
class UserConfirmViewSet(ModelViewSet):
    """
    ModelViewSet for confirming client's emails.
    """
    serializer_class = UserConfirmSerializer
    http_method_names = ['post']

    def get_queryset(self):
        return Token.objects.filter(user=self.request.user)


class UserPasswordViewSet(ModelViewSet):
    serializer_class = UserPasswordSerializer
    permission_classes = [IsAuthenticatedClient | IsAuthenticatedSupplier]
    http_method_names = ['patch']

    def get_queryset(self):
        return User.objects.filter(email=self.request.user)
