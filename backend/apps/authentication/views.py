"""
Authentication API views
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from datetime import datetime, timedelta

from .serializers import (
    LoginSerializer,
    UserInfoSerializer,
    RefreshTokenSerializer,
    PermissionSerializer
)
from .jwt_utils import JWTHandler, get_client_ip, get_user_agent
from .models import RefreshToken


class LoginView(APIView):
    """
    POST /api/auth/login/

    Authenticate user with email and password
    Returns access token, refresh token, and user information

    Request:
    {
        "email": "admin@university.edu",
        "password": "password123"
    }

    Response:
    {
        "success": true,
        "message": "Login successful",
        "data": {
            "user": {...},
            "tokens": {
                "access": "eyJ...",
                "refresh": "random_token_string"
            },
            "redirect_url": "/superadmin/dashboard"
        }
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # Validate credentials
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid credentials',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']

        # Generate JWT access token
        access_token = JWTHandler.generate_access_token(user)

        # Generate opaque refresh token
        refresh_token_value = RefreshToken.generate_token()

        # Store refresh token in database
        refresh_token = RefreshToken.objects.create(
            user=user,
            token=refresh_token_value,
            expires_at=datetime.utcnow() + timedelta(
                seconds=settings.JWT_SETTINGS['REFRESH_TOKEN_LIFETIME']
            ),
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request)
        )

        # Serialize user information
        user_serializer = UserInfoSerializer(user, context={'request': request})

        # Determine redirect URL based on role
        primary_role = user.get_primary_role()
        redirect_url = '/dashboard'  # Default

        if user.is_superuser or (primary_role and primary_role.name == 'Superadmin'):
            redirect_url = '/superadmin/dashboard'
        elif primary_role:
            role_name = primary_role.name.lower()
            redirect_url = f'/{role_name}/dashboard'

        return Response({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': user_serializer.data,
                'tokens': {
                    'access': access_token,
                    'refresh': refresh_token_value
                },
                'redirect_url': redirect_url
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/auth/logout/

    Logout user by blacklisting access token and revoking refresh token

    Request:
    {
        "refresh_token": "optional_refresh_token_string"
    }

    Response:
    {
        "success": true,
        "message": "Logout successful"
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Blacklist the current access token
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token = None

        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]

        if token:
            JWTHandler.blacklist_token(
                token,
                request.user,
                reason='User logged out'
            )

        # Revoke refresh token if provided
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            RefreshToken.objects.filter(
                token=refresh_token,
                user=request.user,
                is_revoked=False
            ).update(is_revoked=True)

        # Clear user permission cache
        request.user.clear_permission_cache()

        return Response({
            'success': True,
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    """
    POST /api/auth/refresh/

    Refresh access token using refresh token
    Implements token rotation for security

    Request:
    {
        "refresh_token": "current_refresh_token_string"
    }

    Response:
    {
        "success": true,
        "message": "Token refreshed successfully",
        "data": {
            "tokens": {
                "access": "new_access_token",
                "refresh": "new_refresh_token"
            }
        }
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Refresh token is required',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        refresh_token_value = serializer.validated_data['refresh_token']

        # Validate refresh token
        try:
            refresh_token = RefreshToken.objects.select_related('user').get(
                token=refresh_token_value,
                is_revoked=False
            )
        except RefreshToken.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid or revoked refresh token'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Check if token is expired
        if refresh_token.expires_at < datetime.utcnow():
            return Response({
                'success': False,
                'message': 'Refresh token has expired'
            }, status=status.HTTP_401_UNAUTHORIZED)

        user = refresh_token.user

        # Check if user is still active
        if not user.is_active:
            return Response({
                'success': False,
                'message': 'User account is inactive'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Generate new access token
        new_access_token = JWTHandler.generate_access_token(user)

        # Generate new refresh token (token rotation)
        new_refresh_token_value = RefreshToken.generate_token()
        new_refresh_token = RefreshToken.objects.create(
            user=user,
            token=new_refresh_token_value,
            expires_at=datetime.utcnow() + timedelta(
                seconds=settings.JWT_SETTINGS['REFRESH_TOKEN_LIFETIME']
            ),
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request)
        )

        # Revoke old refresh token and link to new one
        refresh_token.is_revoked = True
        refresh_token.replaced_by = new_refresh_token
        refresh_token.save(update_fields=['is_revoked', 'replaced_by'])

        return Response({
            'success': True,
            'message': 'Token refreshed successfully',
            'data': {
                'tokens': {
                    'access': new_access_token,
                    'refresh': new_refresh_token_value
                }
            }
        }, status=status.HTTP_200_OK)


class MyPermissionsView(APIView):
    """
    GET /api/auth/my-permissions/

    Get current user's permissions
    Used by frontend to determine which features to show

    Response:
    {
        "success": true,
        "data": {
            "user": {
                "id": 1,
                "email": "admin@university.edu",
                "role": "Superadmin",
                "college_id": 1
            },
            "permissions": [
                {
                    "id": 1,
                    "name": "View General Setting",
                    "codename": "view_general_setting",
                    "module": "setting"
                },
                ...
            ]
        }
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        permissions = user.get_permissions()

        # Get primary role
        primary_role = user.get_primary_role()

        return Response({
            'success': True,
            'data': {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'full_name': user.get_full_name(),
                    'role': primary_role.name if primary_role else None,
                    'role_id': primary_role.id if primary_role else None,
                    'college_id': user.college_id,
                    'is_superuser': user.is_superuser
                },
                'permissions': permissions
            }
        }, status=status.HTTP_200_OK)


class MyProfileView(APIView):
    """
    GET /api/auth/my-profile/

    Get current user's detailed profile information

    Response:
    {
        "success": true,
        "data": {
            "user": {...full user details...}
        }
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserInfoSerializer(request.user, context={'request': request})

        return Response({
            'success': True,
            'data': {
                'user': serializer.data
            }
        }, status=status.HTTP_200_OK)


class VerifyTokenView(APIView):
    """
    POST /api/auth/verify-token/

    Verify if current access token is valid
    Useful for frontend to check token status

    Response:
    {
        "success": true,
        "message": "Token is valid",
        "data": {
            "user_id": 1,
            "email": "admin@university.edu",
            "exp": 1699999999
        }
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # If we reach here, token is valid (authentication passed)
        token_payload = getattr(request, 'token_payload', {})

        return Response({
            'success': True,
            'message': 'Token is valid',
            'data': {
                'user_id': token_payload.get('user_id'),
                'email': token_payload.get('email'),
                'exp': token_payload.get('exp'),
                'role': token_payload.get('role'),
                'college_id': token_payload.get('college_id')
            }
        }, status=status.HTTP_200_OK)
