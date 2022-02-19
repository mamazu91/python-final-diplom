from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, OpenApiTypes
from rest_framework.viewsets import ModelViewSet
from contacts.models import User
from .serializers import ClientRegisterSerializer, ClientEmailConfirmSerializer, PasswordChangeSerializer
from rest_framework.authtoken.models import Token
from contacts.permissions import IsAuthenticatedClient
from shops.permissions import IsAuthenticatedSupplier
from rest_framework.response import Response


@extend_schema(
    summary='Register',
    description='Register a new account. '
                'Email with confirmation token is going to be sent to the specified email address. '
                'Account will remain unconfirmed until you confirm the specified email '
                'by sending the confirmation token to the /api/v1/confirm/ endpoint.',
    request={'application/json': ClientRegisterSerializer},
    responses={
        201: OpenApiResponse(response=ClientRegisterSerializer),
        400: OpenApiResponse(description='Request body is incorrect')
    }
)
class ClientRegisterViewSet(ModelViewSet):
    """
    ModelViewSet for registering clients.
    Endpoint: /api/v1/client/reg/
    """
    queryset = User.objects.all()
    serializer_class = ClientRegisterSerializer
    http_method_names = ['post']


@extend_schema(
    summary='Confirm email address',
    description='Confirm your email address by entering the token '
                'that was sent to the email specified upon registration.',
    request={'application/json': ClientEmailConfirmSerializer},
    responses={
        201: OpenApiResponse(response=ClientEmailConfirmSerializer),
        400: OpenApiResponse(description='Request body is incorrect')
    }
)
class ClientEmailConfirmViewSet(ModelViewSet):
    """
    ModelViewSet for confirming clients emails.
    Endpoint: /api/v1/client/confirm/
    """
    serializer_class = ClientEmailConfirmSerializer
    http_method_names = ['post']

    def get_queryset(self):
        return Token.objects.filter(user=self.request.user)


@extend_schema(
    summary='Change password',
    description='Change your password.',
    request={'application/json': PasswordChangeSerializer},
    parameters=(
            [
                OpenApiParameter(
                    "id",
                    OpenApiTypes.INT,
                    OpenApiParameter.PATH,
                    exclude=True
                )
            ]
    ),
    responses={
        200: OpenApiResponse(response=PasswordChangeSerializer),
        400: OpenApiResponse(description='Request body is incorrect'),
        401: OpenApiResponse(description='Header is missing authorization token'),
        403: OpenApiResponse(description='Your account does not have enough permissions for this action')
    },
)
class PasswordChangeViewSet(ModelViewSet):
    """
    ModelViewSet for changing clients or suppliers passwords.
    Endpoint: /api/v1/client/pwd/ and /api/v1/partner/pwd/
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticatedClient | IsAuthenticatedSupplier]
    http_method_names = ['patch']

    def get_object(self):
        return User.objects.get(email=self.request.user)

    def patch(self, request):
        instance = self.get_object()
        serializer = super().get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
