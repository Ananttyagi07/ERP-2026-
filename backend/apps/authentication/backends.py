"""
Custom authentication backends for JWT
"""
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .jwt_utils import JWTHandler
import jwt

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication backend for DRF
    Extracts and validates JWT from Authorization header
    """

    def authenticate(self, request):
        """
        Authenticate the request and return (user, token) tuple
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header:
            return None

        try:
            # Extract token from "Bearer <token>"
            auth_parts = auth_header.split()

            if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
                return None

            token = auth_parts[1]

            # Decode and validate token
            payload = JWTHandler.decode_access_token(token)

            # Get user from payload
            user_id = payload.get('user_id')
            if not user_id:
                raise AuthenticationFailed('Invalid token payload')

            try:
                user = User.objects.select_related('college').get(
                    id=user_id,
                    is_active=True
                )
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found or inactive')

            # Attach token payload to request for easy access
            request.token_payload = payload

            return (user, token)

        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(str(e))
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')

    def authenticate_header(self, request):
        """
        Return WWW-Authenticate header for 401 responses
        """
        return 'Bearer realm="api"'
