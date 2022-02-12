from rest_framework.viewsets import ModelViewSet
from contacts.models import User
from .serializers import UserRegisterSerializer, UserConfirmSerializer, UserPasswordSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.authtoken.models import Token
from contacts.permissions import IsAuthenticatedClient
from shops.permissions import IsAuthenticatedSupplier


@extend_schema(
    summary='Register a client',
    description="Register a client by providing the necessary information. "
                "Confirmation email is going to be sent to the specified email.",
    request={
        'application/json': UserRegisterSerializer},
    responses={
        201: OpenApiResponse(response=UserRegisterSerializer),
        400: OpenApiResponse(description='Bad Request')
    }
)
class UserRegisterViewSet(ModelViewSet):
    """
    ModelViewSet for registering clients.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']


@extend_schema(
    summary="Confirm client's email",
    description="Confirm client's email by specifying the token "
                "that was sent to the client's email upon registration.",
    request={
        'application/json': UserConfirmSerializer},
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


@extend_schema(
    summary="Change client's or supplier's password",
    description='Change password of the specified user.',
    request={'application/json': UserPasswordSerializer},
    responses={
        200: OpenApiResponse(response=UserPasswordSerializer),
        400: OpenApiResponse(description='Bad Request'),
        401: OpenApiResponse(description='Unauthorized'),
        403: OpenApiResponse(description='Forbidden')
    }
)
class UserPasswordViewSet(ModelViewSet):
    """
    ModelViewSet for changing client's or supplier's passwords.
    """
    serializer_class = UserPasswordSerializer
    permission_classes = [IsAuthenticatedClient | IsAuthenticatedSupplier]
    http_method_names = ['patch']

    def get_queryset(self):
        return User.objects.filter(email=self.request.user)
