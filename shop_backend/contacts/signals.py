from django.conf import settings
from django.core.mail import send_mail as send_confirm_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import User


@receiver(post_save, sender=User, dispatch_uid='contacts.signals.contact_post_save')
def contact_create_save(sender, instance, created, **kwargs):
    if created:
        confirmation_token = Token.objects.create(user=instance)
        send_confirm_mail(
            'Finish your registration',
            f'Greetings!\n\n'
            f'In order to confirm your account, '
            f'please send the following token to /api/v1/confirm/ endpoint: {confirmation_token}',
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=True
        )
