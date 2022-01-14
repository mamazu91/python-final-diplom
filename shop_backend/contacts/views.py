from rest_framework.viewsets import ModelViewSet
from contacts.models import User
from .serializers import UserRegisterSerializer, UserConfirmSerializer
from rest_framework.authtoken.models import Token


class UserRegisterViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']


class UserConfirmViewSet(ModelViewSet):
    serializer_class = UserConfirmSerializer
    http_method_names = ['post']

    def get_queryset(self):
        return Token.objects.filter(user=self.request.user)
