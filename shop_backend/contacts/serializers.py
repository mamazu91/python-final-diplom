from rest_framework import serializers
from contacts.models import User
from django.db import transaction
from rest_framework.exceptions import ValidationError
from orders.models import Order
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail as send_confirm_mail
from shop_backend import settings
from django.shortcuts import get_object_or_404


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'password', 'password_repeat', 'company',
                  'position']

    def create(self, validated_data):
        with transaction.atomic():
            new_user, is_new_user_created = User.objects.get_or_create(
                email=validated_data.get('email'),
                defaults={
                    'first_name': validated_data.get('first_name'),
                    'middle_name': validated_data.get('middle_name'),
                    'last_name': validated_data.get('last_name'),
                    'company': validated_data.get('company'),
                    'position': validated_data.get('position')
                }
            )

            if not is_new_user_created:
                raise ValidationError({'results': ['User with this email already exists.']})

            new_user.set_password(validated_data.get('password'))
            new_user.save()

            new_user_basket = Order(
                user=new_user
            )
            new_user_basket.save()

            new_user_confirm_token = Token.objects.create(user=new_user)
            send_confirm_mail(
                f'Netology diploma confirmation email.',
                f'Hello user {new_user.email}! \n\n In order to confirm your account, '
                f'please send this token {new_user_confirm_token} to /api/v1/confirm/ endpoint.',
                settings.EMAIL_HOST_USER,
                [new_user.email],
                fail_silently=True
            )

            return new_user

    def validate(self, data):
        password = data.get('password')
        password_repeat = data.get('password_repeat')
        if password != password_repeat:
            raise ValidationError({'results': ['Passwords are different.']})

        return data


class UserConfirmSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='key')

    class Meta:
        model = User
        fields = ['token']

    def create(self, validated_data):
        request_token = validated_data.pop('key')
        db_token = get_object_or_404(Token, key=request_token)
        user = User.objects.get(email=db_token.user)
        if not user.is_confirmed:
            db_token.delete()
            user.is_confirmed = True
            user.save()
        else:
            raise ValidationError({'results': ['This user has already confirmed his email.']})

        return db_token


class UserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password']

    def update(self, instance, validated_data):
        new_password = validated_data.pop('password')
        if new_password:
            instance.set_password(new_password)
            instance.save()

        return instance

    def validate(self, data):
        if not data.get('password'):
            raise ValidationError({'results': ['Provide a new password.']})

        return data
