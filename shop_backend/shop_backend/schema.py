from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.extensions import OpenApiViewExtension
from rest_framework.authtoken.serializers import AuthTokenSerializer


class AddAuthEndpointDescription(OpenApiViewExtension):
    target_class = 'rest_framework.authtoken.views.obtain_auth_token'

    def view_replacement(self):
        @extend_schema(
            auth=None,
            summary='Authenticate',
            description='Authenticate your user.',
            request={'application/json': AuthTokenSerializer},
            responses={
                200: AuthTokenSerializer,
                400: OpenApiResponse(description='Request body is incorrect')
            }
        )
        class Fixed(self.target_class):
            pass

        return Fixed
