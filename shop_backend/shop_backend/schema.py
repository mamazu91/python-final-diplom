from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.extensions import OpenApiViewExtension
from rest_framework.authtoken.serializers import AuthTokenSerializer


def filter_swagger_paths(endpoints):
    filtered_paths = []
    for (path, path_regex, method, callback) in endpoints:
        if path == '/api/v1/client/pwd/{pk}/':
            filtered_paths.append(('/api/v1/client/pwd/', path_regex, method, callback))
        elif path == '/api/v1/partner/pwd/{pk}/':
            filtered_paths.append(('/api/v1/partner/pwd/', path_regex, method, callback))
        elif path == '/api/v1/client/basket/{pk}/':
            filtered_paths.append(('/api/v1/client/basket/', path_regex, method, callback))
        else:
            filtered_paths.append((path, path_regex, method, callback))
    return filtered_paths


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
            },
            tags=['common']
        )
        class Fixed(self.target_class):
            pass

        return Fixed
