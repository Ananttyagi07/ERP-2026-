import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication backend for Django REST Framework.
    """

    def authenticate(self, request):
        """
        Authenticate the request using JWT token from Authorization header.
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header:
            return None

        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SETTINGS['ALGORITHM'],
                options={"verify_signature": False}  # We'll verify signature separately
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(_('Token has expired'))
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed(_('Invalid token'))

        # Verify signature with secret key
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_SETTINGS['ALGORITHM']]
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(_('Token has expired'))
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed(_('Invalid token'))

        user_id = payload.get('user_id')
        if not user_id:
            raise exceptions.AuthenticationFailed(_('Invalid token payload'))

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('User not found'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User account is disabled'))

        return (user, token)

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response.
        """
        return 'Bearer'
