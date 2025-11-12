"""
Enterprise Security Views
Enhanced authentication with MFA, session management, audit logging, and rate limiting
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from datetime import datetime, timedelta
import secrets

from .serializers import LoginSerializer, UserInfoSerializer
from .jwt_utils import JWTHandler
from .models import RefreshToken
from .models_security import SecurityAuditLog, UserSession, UserMFA, OTPCode
from .utils import (
    get_client_ip,
    get_user_agent,
    get_device_details,
    generate_device_fingerprint,
    get_geolocation,
    calculate_trust_score,
    detect_suspicious_login,
    should_require_mfa,
    send_otp_sms,
    send_otp_email
)


class EnhancedLoginView(APIView):
    """
    POST /api/auth/login/

    Enterprise-grade login with:
    - Rate limiting (5 attempts/min per IP)
    - Audit logging (all attempts logged)
    - Device fingerprinting
    - Geolocation tracking
    - Trust scoring
    - Suspicious login detection
    - MFA requirement detection
    - Session management

    Request:
    {
        "email": "admin@university.edu",
        "password": "password123"
    }

    Response (Success - No MFA Required):
    {
        "success": true,
        "message": "Login successful",
        "data": {
            "user": {...},
            "tokens": {
                "access": "eyJ...",
                "refresh": "random_token"
            },
            "session_id": "uuid-here",
            "redirect_url": "/superadmin/dashboard"
        }
    }

    Response (Success - MFA Required):
    {
        "success": true,
        "message": "MFA verification required",
        "data": {
            "mfa_required": true,
            "mfa_methods": ["totp", "sms", "email"],
            "session_id": "temp-uuid-for-mfa-verification",
            "trust_score": 45
        }
    }
    """
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    @method_decorator(ratelimit(key='user_or_ip', rate='10/h', method='POST', block=True))
    def post(self, request):
        # Get request metadata
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        device_details = get_device_details(request)
        device_fingerprint = generate_device_fingerprint(request)
        geolocation = get_geolocation(ip_address)

        # Validate credentials
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            # Log failed login attempt
            SecurityAuditLog.log(
                'login_failed',
                request,
                user=None,
                success=False,
                failure_reason='Invalid credentials provided',
                action='login',
                metadata={
                    'email': request.data.get('email'),
                    'error': serializer.errors
                }
            )

            return Response({
                'success': False,
                'message': 'Invalid credentials',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']

        # Calculate trust score
        trust_score = calculate_trust_score(user, request)

        # Check if login is suspicious
        is_suspicious = detect_suspicious_login(user, request)

        # Check if MFA is required
        mfa_required = should_require_mfa(user, request)

        # If MFA is required, don't issue tokens yet
        if mfa_required:
            try:
                mfa = user.mfa

                # Generate OTP for non-TOTP methods
                available_methods = ['totp']

                if user.phone:
                    # Generate SMS OTP
                    otp = OTPCode.objects.create(
                        user=user,
                        code_type='sms',
                        phone_number=user.phone
                    )
                    send_otp_sms(user.phone, otp.code)
                    available_methods.append('sms')

                if user.email:
                    # Generate Email OTP
                    otp = OTPCode.objects.create(
                        user=user,
                        code_type='email',
                        email=user.email
                    )
                    send_otp_email(user.email, otp.code)
                    available_methods.append('email')

                # Create temporary session ID for MFA verification
                temp_session_id = secrets.token_urlsafe(32)

                # Log MFA required event
                SecurityAuditLog.log(
                    'mfa_required',
                    request,
                    user=user,
                    success=True,
                    action='login',
                    metadata={
                        'trust_score': trust_score,
                        'is_suspicious': is_suspicious,
                        'available_methods': available_methods,
                        'temp_session_id': temp_session_id
                    }
                )

                # Store temp session ID in cache for verification (10 minutes)
                from django.core.cache import cache
                cache.set(f'mfa_pending:{temp_session_id}', {
                    'user_id': user.id,
                    'device_fingerprint': device_fingerprint,
                    'ip_address': ip_address,
                    'created_at': datetime.utcnow().isoformat()
                }, timeout=600)  # 10 minutes

                return Response({
                    'success': True,
                    'message': 'MFA verification required',
                    'data': {
                        'mfa_required': True,
                        'mfa_methods': available_methods,
                        'session_id': temp_session_id,
                        'trust_score': trust_score,
                        'is_suspicious': is_suspicious
                    }
                }, status=status.HTTP_200_OK)

            except UserMFA.DoesNotExist:
                # MFA not configured but required - edge case
                pass

        # MFA not required or not configured - proceed with login
        return self._complete_login(user, request, trust_score, is_suspicious, device_details, device_fingerprint, geolocation)

    def _complete_login(self, user, request, trust_score, is_suspicious, device_details, device_fingerprint, geolocation):
        """Complete login process - issue tokens and create session"""

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

        # Create user session
        session = UserSession.objects.create(
            user=user,
            session_id=secrets.token_urlsafe(32),
            refresh_token=refresh_token,
            ip_address=get_client_ip(request),
            country=geolocation.get('country', ''),
            country_code=geolocation.get('country_code', ''),
            city=geolocation.get('city', ''),
            latitude=geolocation.get('latitude'),
            longitude=geolocation.get('longitude'),
            device_type=device_details['type'],
            device_brand=device_details.get('brand', ''),
            device_model=device_details.get('model', ''),
            device_fingerprint=device_fingerprint,
            device_name=device_details['name'],
            browser=device_details['browser']['family'],
            browser_version=device_details['browser']['version'],
            os=device_details['os']['family'],
            os_version=device_details['os']['version'],
            user_agent=get_user_agent(request),
            status='active',
            is_suspicious=is_suspicious,
            trust_score=trust_score,
            login_method='password',
            expires_at=datetime.utcnow() + timedelta(
                seconds=settings.JWT_SETTINGS['REFRESH_TOKEN_LIFETIME']
            )
        )

        # Log successful login
        SecurityAuditLog.log(
            'login_success',
            request,
            user=user,
            success=True,
            action='login',
            metadata={
                'session_id': session.session_id,
                'trust_score': trust_score,
                'is_suspicious': is_suspicious,
                'device': device_details['name'],
                'location': f"{geolocation.get('city', '')}, {geolocation.get('country', '')}"
            }
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
                'session_id': session.session_id,
                'redirect_url': redirect_url,
                'trust_score': trust_score
            }
        }, status=status.HTTP_200_OK)


class MFAVerifyView(APIView):
    """
    POST /api/auth/mfa/verify/

    Verify MFA code and complete login

    Request:
    {
        "session_id": "temp-session-id-from-login",
        "method": "totp|sms|email|backup",
        "code": "123456"
    }

    Response (Success):
    {
        "success": true,
        "message": "MFA verification successful",
        "data": {
            "user": {...},
            "tokens": {...},
            "session_id": "real-session-id",
            "redirect_url": "/dashboard"
        }
    }
    """
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=True))
    def post(self, request):
        session_id = request.data.get('session_id')
        method = request.data.get('method')
        code = request.data.get('code')

        if not all([session_id, method, code]):
            return Response({
                'success': False,
                'message': 'session_id, method, and code are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get pending MFA session from cache
        from django.core.cache import cache
        pending_session = cache.get(f'mfa_pending:{session_id}')

        if not pending_session:
            SecurityAuditLog.log(
                'mfa_verification_failed',
                request,
                user=None,
                success=False,
                failure_reason='Invalid or expired session ID',
                action='mfa_verify'
            )

            return Response({
                'success': False,
                'message': 'Invalid or expired session. Please login again.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get user
        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            user = User.objects.get(id=pending_session['user_id'])
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verify MFA code based on method
        verified = False

        try:
            mfa = user.mfa

            if method == 'totp':
                verified = mfa.verify_totp(code)

            elif method == 'backup':
                verified = mfa.use_backup_code(code)

            elif method in ['sms', 'email']:
                # Verify OTP
                try:
                    otp = OTPCode.objects.get(
                        user=user,
                        code=code,
                        code_type=method,
                        is_used=False
                    )
                    if otp.is_valid():
                        otp.mark_as_used()
                        verified = True
                    else:
                        verified = False
                except OTPCode.DoesNotExist:
                    verified = False

        except UserMFA.DoesNotExist:
            return Response({
                'success': False,
                'message': 'MFA not configured for this user'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not verified:
            # Log failed verification
            SecurityAuditLog.log(
                'mfa_verification_failed',
                request,
                user=user,
                success=False,
                failure_reason='Invalid MFA code',
                action='mfa_verify',
                metadata={'method': method}
            )

            return Response({
                'success': False,
                'message': 'Invalid verification code'
            }, status=status.HTTP_400_BAD_REQUEST)

        # MFA verified - complete login
        # Clear pending session
        cache.delete(f'mfa_pending:{session_id}')

        # Log successful MFA verification
        SecurityAuditLog.log(
            'mfa_verification_success',
            request,
            user=user,
            success=True,
            action='mfa_verify',
            metadata={'method': method}
        )

        # Update MFA statistics
        if method == 'totp':
            mfa.totp_last_used = datetime.utcnow()
            mfa.successful_verifications += 1
        elif method == 'sms':
            mfa.sms_last_used = datetime.utcnow()
        elif method == 'email':
            mfa.email_last_used = datetime.utcnow()
        mfa.save()

        # Check if we should trust this device
        device_fingerprint = generate_device_fingerprint(request)
        if request.data.get('trust_device', False):
            if device_fingerprint not in mfa.trusted_device_fingerprints:
                mfa.trusted_device_fingerprints.append(device_fingerprint)
                mfa.save()

        # Complete login (reuse login view logic)
        device_details = get_device_details(request)
        geolocation = get_geolocation(get_client_ip(request))
        trust_score = calculate_trust_score(user, request)

        login_view = EnhancedLoginView()
        return login_view._complete_login(
            user, request, trust_score, False,
            device_details, device_fingerprint, geolocation
        )


class EnhancedLogoutView(APIView):
    """
    POST /api/auth/logout/

    Enhanced logout with session tracking and audit logging

    Request:
    {
        "session_id": "optional-session-id",
        "refresh_token": "optional-refresh-token"
    }

    Response:
    {
        "success": true,
        "message": "Logout successful"
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Get session ID
        session_id = request.data.get('session_id')

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
                user,
                reason='User logged out'
            )

        # Revoke refresh token
        refresh_token_value = request.data.get('refresh_token')
        if refresh_token_value:
            RefreshToken.objects.filter(
                token=refresh_token_value,
                user=user,
                is_revoked=False
            ).update(is_revoked=True)

        # Update session status
        if session_id:
            UserSession.objects.filter(
                session_id=session_id,
                user=user
            ).update(status='expired')

        # Log logout
        SecurityAuditLog.log(
            'logout',
            request,
            user=user,
            success=True,
            action='logout',
            metadata={'session_id': session_id}
        )

        # Clear user permission cache
        user.clear_permission_cache()

        return Response({
            'success': True,
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)


class SessionListView(APIView):
    """
    GET /api/auth/sessions/

    List all active sessions for current user

    Response:
    {
        "success": true,
        "data": {
            "sessions": [
                {
                    "session_id": "abc-123",
                    "device": "Chrome on Windows",
                    "location": "Mumbai, India",
                    "ip_address": "203.0.113.1",
                    "last_activity": "2024-01-15T10:30:00Z",
                    "is_current": true,
                    "is_suspicious": false,
                    "trust_score": 85,
                    "created_at": "2024-01-15T09:00:00Z"
                }
            ]
        }
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get all active sessions
        sessions = UserSession.objects.filter(
            user=user,
            status='active'
        ).order_by('-last_activity')

        # Get current session ID if provided
        current_session_id = request.query_params.get('session_id')

        sessions_data = []
        for session in sessions:
            sessions_data.append({
                'session_id': session.session_id,
                'device': session.device_name,
                'device_type': session.device_type,
                'browser': session.browser,
                'os': session.os,
                'location': f"{session.city}, {session.country}" if session.city else session.country,
                'ip_address': session.ip_address,
                'last_activity': session.last_activity.isoformat(),
                'created_at': session.created_at.isoformat(),
                'is_current': session.session_id == current_session_id,
                'is_suspicious': session.is_suspicious,
                'is_trusted': session.is_trusted,
                'trust_score': session.trust_score
            })

        return Response({
            'success': True,
            'data': {
                'sessions': sessions_data,
                'count': len(sessions_data)
            }
        }, status=status.HTTP_200_OK)


class SessionRevokeView(APIView):
    """
    DELETE /api/auth/sessions/{session_id}/

    Revoke a specific session

    Response:
    {
        "success": true,
        "message": "Session revoked successfully"
    }
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, session_id):
        user = request.user

        try:
            session = UserSession.objects.get(
                session_id=session_id,
                user=user
            )
        except UserSession.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Session not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Revoke session
        session.status = 'revoked'
        session.save()

        # Revoke associated refresh token
        if session.refresh_token:
            session.refresh_token.is_revoked = True
            session.refresh_token.save()

        # Log session revocation
        SecurityAuditLog.log(
            'session_revoked',
            request,
            user=user,
            success=True,
            action='revoke_session',
            metadata={
                'revoked_session_id': session_id,
                'device': session.device_name
            }
        )

        return Response({
            'success': True,
            'message': 'Session revoked successfully'
        }, status=status.HTTP_200_OK)


class SessionRevokeAllView(APIView):
    """
    POST /api/auth/sessions/revoke-all/

    Revoke all sessions except current one

    Request:
    {
        "current_session_id": "keep-this-session"
    }

    Response:
    {
        "success": true,
        "message": "All other sessions revoked",
        "data": {
            "revoked_count": 3
        }
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_session_id = request.data.get('current_session_id')

        # Get all active sessions except current
        query = UserSession.objects.filter(
            user=user,
            status='active'
        )

        if current_session_id:
            query = query.exclude(session_id=current_session_id)

        # Count sessions to revoke
        revoked_count = query.count()

        # Revoke all sessions
        query.update(status='revoked')

        # Revoke associated refresh tokens
        session_ids = list(query.values_list('refresh_token_id', flat=True))
        RefreshToken.objects.filter(
            id__in=session_ids
        ).update(is_revoked=True)

        # Log mass revocation
        SecurityAuditLog.log(
            'sessions_revoked_all',
            request,
            user=user,
            success=True,
            action='revoke_all_sessions',
            metadata={
                'revoked_count': revoked_count,
                'kept_session': current_session_id
            }
        )

        return Response({
            'success': True,
            'message': f'Revoked {revoked_count} session(s) successfully',
            'data': {
                'revoked_count': revoked_count
            }
        }, status=status.HTTP_200_OK)
