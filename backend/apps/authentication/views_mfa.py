"""
MFA (Multi-Factor Authentication) Setup and Management APIs
Supports TOTP, SMS, Email with backup codes and trusted devices
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from datetime import datetime
import qrcode
import io
import base64

from .models_security import UserMFA, OTPCode, SecurityAuditLog
from .utils import (
    send_otp_sms,
    send_otp_email,
    generate_device_fingerprint
)


class MFAStatusView(APIView):
    """
    GET /api/auth/mfa/status/

    Get current MFA status for user

    Response:
    {
        "success": true,
        "data": {
            "mfa_enabled": true,
            "mfa_enforced": false,
            "primary_method": "totp",
            "available_methods": ["totp", "sms", "email"],
            "backup_codes_remaining": 8,
            "trusted_devices": 2,
            "last_used": "2024-01-15T10:30:00Z"
        }
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            mfa = user.mfa

            # Determine available methods
            available_methods = []
            if mfa.totp_secret:
                available_methods.append('totp')
            if user.phone:
                available_methods.append('sms')
            if user.email:
                available_methods.append('email')

            return Response({
                'success': True,
                'data': {
                    'mfa_enabled': mfa.is_enabled,
                    'mfa_enforced': mfa.is_enforced,
                    'primary_method': mfa.primary_method,
                    'available_methods': available_methods,
                    'backup_codes_remaining': len([c for c in mfa.backup_codes if c]),
                    'trusted_devices': len(mfa.trusted_device_fingerprints),
                    'totp_last_used': mfa.totp_last_used.isoformat() if mfa.totp_last_used else None,
                    'sms_last_used': mfa.sms_last_used.isoformat() if mfa.sms_last_used else None,
                    'email_last_used': mfa.email_last_used.isoformat() if mfa.email_last_used else None,
                    'successful_verifications': mfa.successful_verifications,
                    'failed_attempts': mfa.failed_attempts
                }
            }, status=status.HTTP_200_OK)

        except UserMFA.DoesNotExist:
            return Response({
                'success': True,
                'data': {
                    'mfa_enabled': False,
                    'mfa_enforced': False,
                    'available_methods': []
                }
            }, status=status.HTTP_200_OK)


class MFASetupInitiateView(APIView):
    """
    POST /api/auth/mfa/setup/initiate/

    Initiate MFA setup - generate TOTP secret and QR code

    Request:
    {
        "method": "totp|sms|email"
    }

    Response (TOTP):
    {
        "success": true,
        "data": {
            "method": "totp",
            "secret": "BASE32SECRET",
            "qr_code": "data:image/png;base64,...",
            "manual_entry_key": "XXXX-XXXX-XXXX-XXXX",
            "issuer": "University ERP"
        }
    }

    Response (SMS/Email):
    {
        "success": true,
        "data": {
            "method": "sms",
            "message": "OTP sent to +91******1234"
        }
    }
    """
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='user', rate='5/h', method='POST', block=True))
    def post(self, request):
        user = request.user
        method = request.data.get('method', 'totp')

        if method not in ['totp', 'sms', 'email']:
            return Response({
                'success': False,
                'message': 'Invalid method. Must be: totp, sms, or email'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get or create MFA settings
        mfa, created = UserMFA.objects.get_or_create(user=user)

        if method == 'totp':
            # Generate TOTP secret
            secret = mfa.generate_totp_secret()
            mfa.save()

            # Get provisioning URI
            uri = mfa.get_totp_uri()

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(uri)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()

            # Format secret for manual entry (XXXX-XXXX-XXXX-XXXX)
            manual_key = '-'.join([secret[i:i+4] for i in range(0, len(secret), 4)])

            # Log MFA setup initiation
            SecurityAuditLog.log(
                'mfa_setup_initiated',
                request,
                user=user,
                success=True,
                action='mfa_setup',
                metadata={'method': 'totp'}
            )

            return Response({
                'success': True,
                'data': {
                    'method': 'totp',
                    'secret': secret,
                    'qr_code': f'data:image/png;base64,{img_str}',
                    'manual_entry_key': manual_key,
                    'issuer': 'University ERP',
                    'account': user.email
                }
            }, status=status.HTTP_200_OK)

        elif method == 'sms':
            if not user.phone:
                return Response({
                    'success': False,
                    'message': 'Phone number not configured for this user'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Generate OTP
            otp = OTPCode.objects.create(
                user=user,
                code_type='sms',
                phone_number=user.phone
            )

            # Send OTP
            send_otp_sms(user.phone, otp.code)

            # Mask phone number
            masked_phone = f"{user.phone[:3]}******{user.phone[-4:]}"

            # Log MFA setup initiation
            SecurityAuditLog.log(
                'mfa_setup_initiated',
                request,
                user=user,
                success=True,
                action='mfa_setup',
                metadata={'method': 'sms'}
            )

            return Response({
                'success': True,
                'data': {
                    'method': 'sms',
                    'message': f'OTP sent to {masked_phone}'
                }
            }, status=status.HTTP_200_OK)

        elif method == 'email':
            # Generate OTP
            otp = OTPCode.objects.create(
                user=user,
                code_type='email',
                email=user.email
            )

            # Send OTP
            send_otp_email(user.email, otp.code)

            # Mask email
            email_parts = user.email.split('@')
            masked_email = f"{email_parts[0][:2]}***@{email_parts[1]}"

            # Log MFA setup initiation
            SecurityAuditLog.log(
                'mfa_setup_initiated',
                request,
                user=user,
                success=True,
                action='mfa_setup',
                metadata={'method': 'email'}
            )

            return Response({
                'success': True,
                'data': {
                    'method': 'email',
                    'message': f'OTP sent to {masked_email}'
                }
            }, status=status.HTTP_200_OK)


class MFASetupCompleteView(APIView):
    """
    POST /api/auth/mfa/setup/complete/

    Complete MFA setup by verifying code

    Request:
    {
        "method": "totp|sms|email",
        "code": "123456"
    }

    Response:
    {
        "success": true,
        "message": "MFA enabled successfully",
        "data": {
            "backup_codes": ["CODE1", "CODE2", ...],
            "warning": "Save these backup codes securely"
        }
    }
    """
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='user', rate='10/h', method='POST', block=True))
    def post(self, request):
        user = request.user
        method = request.data.get('method')
        code = request.data.get('code')

        if not method or not code:
            return Response({
                'success': False,
                'message': 'method and code are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            mfa = user.mfa
        except UserMFA.DoesNotExist:
            return Response({
                'success': False,
                'message': 'MFA setup not initiated. Call /setup/initiate/ first.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verify code based on method
        verified = False

        if method == 'totp':
            if not mfa.totp_secret:
                return Response({
                    'success': False,
                    'message': 'TOTP not configured. Call /setup/initiate/ first.'
                }, status=status.HTTP_400_BAD_REQUEST)

            verified = mfa.verify_totp(code)

        elif method in ['sms', 'email']:
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
            except OTPCode.DoesNotExist:
                verified = False

        if not verified:
            mfa.failed_attempts += 1
            mfa.save()

            # Log failed setup
            SecurityAuditLog.log(
                'mfa_setup_failed',
                request,
                user=user,
                success=False,
                failure_reason='Invalid verification code',
                action='mfa_setup',
                metadata={'method': method}
            )

            return Response({
                'success': False,
                'message': 'Invalid verification code'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Code verified - enable MFA
        mfa.is_enabled = True
        mfa.primary_method = method

        # Generate backup codes if not already generated
        backup_codes = mfa.backup_codes
        if not backup_codes or len(backup_codes) == 0:
            backup_codes = mfa.generate_backup_codes()

        mfa.save()

        # Log successful MFA setup
        SecurityAuditLog.log(
            'mfa_enabled',
            request,
            user=user,
            success=True,
            action='mfa_setup',
            metadata={'method': method}
        )

        return Response({
            'success': True,
            'message': 'MFA enabled successfully',
            'data': {
                'backup_codes': backup_codes,
                'warning': 'Save these backup codes securely. They will not be shown again.'
            }
        }, status=status.HTTP_200_OK)


class MFADisableView(APIView):
    """
    POST /api/auth/mfa/disable/

    Disable MFA (requires password confirmation)

    Request:
    {
        "password": "current_password",
        "reason": "optional reason"
    }

    Response:
    {
        "success": true,
        "message": "MFA disabled successfully"
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        password = request.data.get('password')
        reason = request.data.get('reason', 'User requested')

        if not password:
            return Response({
                'success': False,
                'message': 'Password is required to disable MFA'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verify password
        if not user.check_password(password):
            # Log failed attempt
            SecurityAuditLog.log(
                'mfa_disable_failed',
                request,
                user=user,
                success=False,
                failure_reason='Invalid password',
                action='mfa_disable'
            )

            return Response({
                'success': False,
                'message': 'Invalid password'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            mfa = user.mfa

            # Check if MFA is enforced (cannot be disabled)
            if mfa.is_enforced:
                return Response({
                    'success': False,
                    'message': 'MFA is enforced by administrator and cannot be disabled'
                }, status=status.HTTP_403_FORBIDDEN)

            # Disable MFA
            mfa.is_enabled = False
            mfa.save()

            # Log MFA disabled
            SecurityAuditLog.log(
                'mfa_disabled',
                request,
                user=user,
                success=True,
                action='mfa_disable',
                metadata={'reason': reason}
            )

            return Response({
                'success': True,
                'message': 'MFA disabled successfully'
            }, status=status.HTTP_200_OK)

        except UserMFA.DoesNotExist:
            return Response({
                'success': False,
                'message': 'MFA is not enabled'
            }, status=status.HTTP_400_BAD_REQUEST)


class MFARegenerateBackupCodesView(APIView):
    """
    POST /api/auth/mfa/backup-codes/regenerate/

    Regenerate backup codes (requires password or MFA verification)

    Request:
    {
        "password": "current_password"
    }

    Response:
    {
        "success": true,
        "data": {
            "backup_codes": ["CODE1", "CODE2", ...],
            "warning": "Old backup codes are now invalid"
        }
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        password = request.data.get('password')

        if not password:
            return Response({
                'success': False,
                'message': 'Password is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verify password
        if not user.check_password(password):
            return Response({
                'success': False,
                'message': 'Invalid password'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            mfa = user.mfa

            # Generate new backup codes
            backup_codes = mfa.generate_backup_codes()
            mfa.save()

            # Log backup codes regeneration
            SecurityAuditLog.log(
                'mfa_backup_codes_regenerated',
                request,
                user=user,
                success=True,
                action='mfa_regenerate_codes'
            )

            return Response({
                'success': True,
                'data': {
                    'backup_codes': backup_codes,
                    'warning': 'Old backup codes are now invalid. Save these new codes securely.'
                }
            }, status=status.HTTP_200_OK)

        except UserMFA.DoesNotExist:
            return Response({
                'success': False,
                'message': 'MFA is not enabled'
            }, status=status.HTTP_400_BAD_REQUEST)


class MFATrustedDevicesView(APIView):
    """
    GET /api/auth/mfa/trusted-devices/

    List trusted devices

    Response:
    {
        "success": true,
        "data": {
            "trusted_devices": [
                {
                    "fingerprint": "abc123...",
                    "device_name": "Chrome on Windows",
                    "added_at": "2024-01-15T10:30:00Z"
                }
            ]
        }
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            mfa = user.mfa

            # Get device info for each fingerprint
            from .models_security import UserSession
            trusted_devices = []

            for fingerprint in mfa.trusted_device_fingerprints:
                # Find most recent session with this fingerprint
                session = UserSession.objects.filter(
                    user=user,
                    device_fingerprint=fingerprint
                ).order_by('-created_at').first()

                if session:
                    trusted_devices.append({
                        'fingerprint': fingerprint[:16] + '...',  # Truncate for display
                        'device_name': session.device_name,
                        'device_type': session.device_type,
                        'browser': session.browser,
                        'os': session.os,
                        'last_used': session.last_activity.isoformat()
                    })

            return Response({
                'success': True,
                'data': {
                    'trusted_devices': trusted_devices,
                    'count': len(trusted_devices)
                }
            }, status=status.HTTP_200_OK)

        except UserMFA.DoesNotExist:
            return Response({
                'success': True,
                'data': {
                    'trusted_devices': [],
                    'count': 0
                }
            }, status=status.HTTP_200_OK)


class MFARemoveTrustedDeviceView(APIView):
    """
    DELETE /api/auth/mfa/trusted-devices/{fingerprint}/

    Remove a trusted device

    Response:
    {
        "success": true,
        "message": "Trusted device removed successfully"
    }
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, fingerprint):
        user = request.user

        try:
            mfa = user.mfa

            # Check if device is in trusted list
            if fingerprint in mfa.trusted_device_fingerprints:
                mfa.trusted_device_fingerprints.remove(fingerprint)
                mfa.save()

                # Log device removal
                SecurityAuditLog.log(
                    'mfa_trusted_device_removed',
                    request,
                    user=user,
                    success=True,
                    action='mfa_remove_device',
                    metadata={'fingerprint': fingerprint[:16]}
                )

                return Response({
                    'success': True,
                    'message': 'Trusted device removed successfully'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Device not found in trusted list'
                }, status=status.HTTP_404_NOT_FOUND)

        except UserMFA.DoesNotExist:
            return Response({
                'success': False,
                'message': 'MFA is not enabled'
            }, status=status.HTTP_400_BAD_REQUEST)
