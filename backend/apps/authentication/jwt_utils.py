"""
JWT Token utilities for authentication
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from .models import BlacklistedToken


class JWTHandler:
    """
    JWT token generation and validation handler
    """

    @staticmethod
    def generate_access_token(user):
        """
        Generate JWT access token for authenticated user
        Includes user info, role, and permissions
        """
        now = datetime.utcnow()
        expiry = now + timedelta(seconds=settings.JWT_SETTINGS['ACCESS_TOKEN_LIFETIME'])

        payload = {
            'user_id': user.id,
            'email': user.email,
            'username': user.username,
            'college_id': user.college_id,
            'is_superuser': user.is_superuser,
            'exp': expiry,
            'iat': now,
            'type': 'access'
        }

        # Add role information
        primary_role = user.get_primary_role()
        if primary_role:
            payload['role'] = primary_role.name
            payload['role_id'] = primary_role.id

        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.JWT_SETTINGS['ALGORITHM']  # Use configured algorithm
        )

        return token

    @staticmethod
    def decode_access_token(token):
        """
        Decode and validate JWT access token
        Returns payload if valid, raises exception if invalid
        """
        try:
            # Check if token is blacklisted
            if JWTHandler.is_token_blacklisted(token):
                raise jwt.InvalidTokenError('Token has been revoked')

            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_SETTINGS['ALGORITHM']]  # Use configured algorithm
            )

            if payload.get('type') != 'access':
                raise jwt.InvalidTokenError('Invalid token type')

            return payload

        except jwt.ExpiredSignatureError:
            raise jwt.InvalidTokenError('Token has expired')
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f'Invalid token: {str(e)}')

    @staticmethod
    def is_token_blacklisted(token):
        """
        Check if token is blacklisted
        Uses cache for performance
        """
        cache_key = f'blacklisted_token_{token[:50]}'
        is_blacklisted = cache.get(cache_key)

        if is_blacklisted is None:
            is_blacklisted = BlacklistedToken.objects.filter(
                token=token
            ).exists()
            cache.set(cache_key, is_blacklisted, timeout=3600)  # Cache for 1 hour

        return is_blacklisted

    @staticmethod
    def blacklist_token(token, user, reason=''):
        """
        Add token to blacklist
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_SETTINGS['ALGORITHM']],  # Use configured algorithm
                options={"verify_exp": False}  # Don't verify expiry for blacklisting
            )

            expires_at = datetime.fromtimestamp(payload['exp'])

            BlacklistedToken.objects.create(
                token=token,
                user=user,
                expires_at=expires_at,
                reason=reason
            )

            # Clear cache
            cache_key = f'blacklisted_token_{token[:50]}'
            cache.set(cache_key, True, timeout=3600)

        except Exception as e:
            print(f"Error blacklisting token: {str(e)}")


def get_client_ip(request):
    """
    Extract client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """
    Extract user agent from request
    """
    return request.META.get('HTTP_USER_AGENT', '')
