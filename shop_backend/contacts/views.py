from rest_framework.viewsets import ModelViewSet
from contacts.models import User
from .serializers import UserRegisterSerializer, UserConfirmSerializer, UserPasswordSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.authtoken.models import Token
from contacts.permissions import IsAuthenticatedClient
from shops.permissions import IsAuthenticatedSupplier


@extend_schema(
    summary='Register',
    description="Register a client and make it unconfirmed. "
                "Email with confirmation token is going to be sent to the specified email address. "
                "Client will remain unconfirmed until he confirms his email "
                "by POSTing the confirmation token to /api/v1/confirm/ endpoint.",
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
    Endpoint: /api/v1/reg/
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']


@extend_schema(
    summary="Confirm email",
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
    ModelViewSet for confirming clients emails.
    Endpoint: /api/v1/confirm/
    """
    serializer_class = UserConfirmSerializer
    http_method_names = ['post']

    def get_queryset(self):
        return Token.objects.filter(user=self.request.user)


@extend_schema(
    summary="Change password",
    description='Change password of specific client or supplier '
                'by providing id uniquely identifying the client or supplier.',
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
    ModelViewSet for changing clients or suppliers passwords.
    Endpoint: api/v1/pwd/
    """
    serializer_class = UserPasswordSerializer
    permission_classes = [IsAuthenticatedClient | IsAuthenticatedSupplier]
    http_method_names = ['patch']

    def get_queryset(self):
        return User.objects.filter(email=self.request.user)
