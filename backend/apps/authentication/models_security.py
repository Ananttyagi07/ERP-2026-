"""
Enterprise Security Models
Audit Logging, Session Management, MFA
"""
from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.core.models import TimeStampedModel
import secrets
import pyotp
from datetime import datetime, timedelta


class SecurityAuditLog(TimeStampedModel):
    """
    Complete audit trail for security and compliance
    Tracks EVERYTHING - logins, permission changes, data access, etc.
    """
    # Event Categories
    CATEGORY_CHOICES = [
        ('authentication', 'Authentication'),
        ('authorization', 'Authorization'),
        ('data_access', 'Data Access'),
        ('data_modification', 'Data Modification'),
        ('system_config', 'System Configuration'),
        ('security', 'Security Event'),
    ]

    # Event Types
    EVENT_TYPES = [
        # Authentication Events
        ('login_success', 'Login Success'),
        ('login_failed', 'Login Failed'),
        ('logout', 'Logout'),
        ('token_refresh', 'Token Refresh'),
        ('token_revoked', 'Token Revoked'),
        ('session_expired', 'Session Expired'),

        # Password Events
        ('password_changed', 'Password Changed'),
        ('password_reset_requested', 'Password Reset Requested'),
        ('password_reset_completed', 'Password Reset Completed'),
        ('password_failed_attempts', 'Password Failed Attempts'),

        # MFA Events
        ('mfa_enabled', 'MFA Enabled'),
        ('mfa_disabled', 'MFA Disabled'),
        ('mfa_verified', 'MFA Verified'),
        ('mfa_failed', 'MFA Failed'),
        ('backup_code_used', 'Backup Code Used'),

        # Permission Events
        ('permission_granted', 'Permission Granted'),
        ('permission_revoked', 'Permission Revoked'),
        ('permission_denied', 'Permission Denied'),
        ('role_assigned', 'Role Assigned'),
        ('role_removed', 'Role Removed'),
        ('role_created', 'Role Created'),
        ('role_deleted', 'Role Deleted'),

        # Data Access Events
        ('data_viewed', 'Data Viewed'),
        ('data_exported', 'Data Exported'),
        ('report_generated', 'Report Generated'),
        ('bulk_operation', 'Bulk Operation'),

        # Data Modification Events
        ('data_created', 'Data Created'),
        ('data_updated', 'Data Updated'),
        ('data_deleted', 'Data Deleted'),
        ('data_restored', 'Data Restored'),

        # System Events
        ('config_changed', 'Configuration Changed'),
        ('user_created', 'User Created'),
        ('user_updated', 'User Updated'),
        ('user_deactivated', 'User Deactivated'),
        ('user_activated', 'User Activated'),

        # Security Events
        ('suspicious_activity', 'Suspicious Activity'),
        ('rate_limit_exceeded', 'Rate Limit Exceeded'),
        ('invalid_token', 'Invalid Token'),
        ('unauthorized_access', 'Unauthorized Access'),
        ('geolocation_blocked', 'Geolocation Blocked'),
        ('device_changed', 'Device Changed'),
    ]

    # Core Fields
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, db_index=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, db_index=True)

    # User Info (store even if user deleted)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    user_email = models.EmailField()
    user_name = models.CharField(max_length=255)
    user_role = models.CharField(max_length=100, blank=True)

    # Request Details
    ip_address = models.GenericIPAddressField(db_index=True)
    user_agent = models.TextField()
    request_method = models.CharField(max_length=10)  # GET, POST, etc.
    request_path = models.CharField(max_length=500)
    request_query = models.TextField(blank=True)  # Query parameters

    # Location (GeoIP)
    country = models.CharField(max_length=100, blank=True)
    country_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Device Info
    device_type = models.CharField(max_length=50, blank=True)  # mobile, desktop, tablet
    device_brand = models.CharField(max_length=100, blank=True)  # Apple, Samsung, etc.
    device_model = models.CharField(max_length=100, blank=True)  # iPhone 12, etc.
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)

    # Event Result
    success = models.BooleanField(default=True, db_index=True)
    status_code = models.IntegerField(null=True, blank=True)
    failure_reason = models.TextField(blank=True)

    # Event Details (flexible JSON storage)
    resource_type = models.CharField(max_length=100, blank=True)  # Student, Teacher, etc.
    resource_id = models.CharField(max_length=100, blank=True)
    resource_name = models.CharField(max_length=255, blank=True)
    action = models.CharField(max_length=100, blank=True)  # view, edit, delete, etc.

    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True)
    changes = models.JSONField(default=dict, blank=True)  # Before/after for modifications

    # Security Flags
    is_suspicious = models.BooleanField(default=False, db_index=True)
    risk_score = models.IntegerField(default=0)  # 0-100
    flagged_for_review = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_audit_logs'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True)

    # Performance Metrics
    response_time_ms = models.IntegerField(null=True, blank=True)
    database_queries = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'security_audit_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'event_type', '-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['ip_address', '-created_at']),
            models.Index(fields=['success', '-created_at']),
            models.Index(fields=['is_suspicious', '-created_at']),
            models.Index(fields=['-created_at', 'event_type']),
        ]

    def __str__(self):
        return f"{self.user_email} - {self.event_type} - {self.created_at}"

    @classmethod
    def log(cls, event_type, request, user=None, success=True, **kwargs):
        """
        Helper method to create audit log entries

        Usage:
            SecurityAuditLog.log(
                'login_success',
                request,
                user=user,
                metadata={'login_method': '2FA'}
            )
        """
        from apps.authentication.utils import (
            get_client_ip,
            get_user_agent,
            detect_device_type,
            get_device_name,
            get_geolocation
        )

        # Get location
        ip = get_client_ip(request)
        geo = get_geolocation(ip)

        # Determine category from event_type
        category_map = {
            'login': 'authentication',
            'logout': 'authentication',
            'token': 'authentication',
            'password': 'authentication',
            'mfa': 'authentication',
            'permission': 'authorization',
            'role': 'authorization',
            'data': 'data_access',
            'config': 'system_config',
            'suspicious': 'security',
        }

        category = 'security'  # default
        for key, cat in category_map.items():
            if key in event_type:
                category = cat
                break

        return cls.objects.create(
            category=category,
            event_type=event_type,
            user=user,
            user_email=user.email if user else kwargs.get('email', request.data.get('email', 'unknown')),
            user_name=user.get_full_name() if user else kwargs.get('user_name', ''),
            user_role=str(user.get_primary_role()) if user else '',
            ip_address=ip,
            user_agent=get_user_agent(request),
            request_method=request.method,
            request_path=request.path,
            request_query=str(request.GET.dict()),
            country=geo.get('country', ''),
            country_code=geo.get('country_code', ''),
            city=geo.get('city', ''),
            region=geo.get('region', ''),
            latitude=geo.get('latitude'),
            longitude=geo.get('longitude'),
            device_type=detect_device_type(request),
            device_brand=kwargs.get('device_brand', ''),
            device_model=get_device_name(request),
            browser=kwargs.get('browser', ''),
            os=kwargs.get('os', ''),
            success=success,
            status_code=kwargs.get('status_code'),
            failure_reason=kwargs.get('failure_reason', ''),
            resource_type=kwargs.get('resource_type', ''),
            resource_id=str(kwargs.get('resource_id', '')),
            resource_name=kwargs.get('resource_name', ''),
            action=kwargs.get('action', ''),
            metadata=kwargs.get('metadata', {}),
            changes=kwargs.get('changes', {}),
            is_suspicious=kwargs.get('is_suspicious', False),
            risk_score=kwargs.get('risk_score', 0),
        )


class UserSession(TimeStampedModel):
    """
    Track active user sessions across devices
    """
    SESSION_STATUS = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
        ('suspicious', 'Suspicious'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sessions')
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    refresh_token = models.OneToOneField(
        'RefreshToken',
        on_delete=models.CASCADE,
        related_name='session'
    )

    # Session Status
    status = models.CharField(max_length=20, choices=SESSION_STATUS, default='active', db_index=True)
    last_activity = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    logout_at = models.DateTimeField(null=True, blank=True)

    # Device Info
    device_type = models.CharField(max_length=50)
    device_brand = models.CharField(max_length=100, blank=True)
    device_model = models.CharField(max_length=100, blank=True)
    device_name = models.CharField(max_length=255)  # "Chrome on Windows"
    device_fingerprint = models.CharField(max_length=255, blank=True, db_index=True)

    # Network Info
    ip_address = models.GenericIPAddressField(db_index=True)
    user_agent = models.TextField()

    # Location
    country = models.CharField(max_length=100, blank=True)
    country_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=100, blank=True)

    # Security Flags
    is_trusted = models.BooleanField(default=False)
    is_suspicious = models.BooleanField(default=False, db_index=True)
    trust_score = models.IntegerField(default=50)  # 0-100
    risk_factors = ArrayField(models.CharField(max_length=100), default=list, blank=True)

    # Metadata
    login_method = models.CharField(max_length=50, default='password')  # password, mfa, oauth
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'user_sessions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status', '-last_activity']),
            models.Index(fields=['device_fingerprint', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.device_name} - {self.status}"

    def is_active(self):
        """Check if session is still active"""
        return (
            self.status == 'active' and
            self.expires_at > datetime.now() and
            not self.is_suspicious
        )

    def mark_suspicious(self, reason):
        """Flag session as suspicious"""
        self.is_suspicious = True
        self.status = 'suspicious'
        self.risk_factors.append(reason)
        self.save()

        # Log security event
        SecurityAuditLog.objects.create(
            category='security',
            event_type='suspicious_activity',
            user=self.user,
            user_email=self.user.email,
            user_name=self.user.get_full_name(),
            ip_address=self.ip_address,
            user_agent=self.user_agent,
            request_method='N/A',
            request_path='/session',
            success=False,
            failure_reason=reason,
            is_suspicious=True,
            metadata={'session_id': self.session_id, 'reason': reason}
        )


class UserMFA(TimeStampedModel):
    """
    Multi-Factor Authentication settings per user
    """
    MFA_TYPES = [
        ('totp', 'TOTP (Google Authenticator)'),
        ('sms', 'SMS OTP'),
        ('email', 'Email OTP'),
    ]

    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='mfa')

    # MFA Status
    is_enabled = models.BooleanField(default=False, db_index=True)
    is_enforced = models.BooleanField(default=False)  # Admin can enforce MFA
    primary_method = models.CharField(max_length=20, choices=MFA_TYPES, default='totp')

    # TOTP Settings
    totp_secret = models.CharField(max_length=100, blank=True)
    totp_verified_at = models.DateTimeField(null=True, blank=True)

    # SMS Settings
    sms_phone = models.CharField(max_length=20, blank=True)
    sms_verified_at = models.DateTimeField(null=True, blank=True)

    # Email Settings
    email_verified_at = models.DateTimeField(null=True, blank=True)

    # Backup Codes
    backup_codes = ArrayField(
        models.CharField(max_length=20),
        default=list,
        blank=True,
        help_text="10 one-time use backup codes"
    )
    backup_codes_generated_at = models.DateTimeField(null=True, blank=True)

    # Trusted Devices
    trusted_device_fingerprints = ArrayField(
        models.CharField(max_length=255),
        default=list,
        blank=True
    )

    # Statistics
    last_used_at = models.DateTimeField(null=True, blank=True)
    total_verifications = models.IntegerField(default=0)
    failed_attempts = models.IntegerField(default=0)
    last_failed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_mfa'
        verbose_name = 'User MFA'
        verbose_name_plural = 'User MFA'

    def __str__(self):
        return f"{self.user.email} - MFA {'Enabled' if self.is_enabled else 'Disabled'}"

    def generate_totp_secret(self):
        """Generate new TOTP secret"""
        self.totp_secret = pyotp.random_base32()
        self.save()
        return self.totp_secret

    def get_totp_uri(self):
        """Get TOTP URI for QR code"""
        if not self.totp_secret:
            self.generate_totp_secret()

        totp = pyotp.TOTP(self.totp_secret)
        return totp.provisioning_uri(
            name=self.user.email,
            issuer_name='University ERP'
        )

    def verify_totp(self, code):
        """Verify TOTP code"""
        if not self.totp_secret:
            return False

        totp = pyotp.TOTP(self.totp_secret)
        is_valid = totp.verify(code, valid_window=1)  # Accept ±30 seconds

        if is_valid:
            self.total_verifications += 1
            self.last_used_at = datetime.now()
            self.failed_attempts = 0
            self.save()
        else:
            self.failed_attempts += 1
            self.last_failed_at = datetime.now()
            self.save()

        return is_valid

    def generate_backup_codes(self, count=10):
        """Generate new backup codes"""
        self.backup_codes = [
            secrets.token_hex(8).upper() for _ in range(count)
        ]
        self.backup_codes_generated_at = datetime.now()
        self.save()
        return self.backup_codes

    def use_backup_code(self, code):
        """Verify and consume a backup code"""
        code = code.upper().strip()

        if code in self.backup_codes:
            self.backup_codes.remove(code)
            self.total_verifications += 1
            self.last_used_at = datetime.now()
            self.save()

            # Log backup code usage
            SecurityAuditLog.objects.create(
                category='authentication',
                event_type='backup_code_used',
                user=self.user,
                user_email=self.user.email,
                user_name=self.user.get_full_name(),
                ip_address='127.0.0.1',  # Will be updated by actual request
                user_agent='',
                request_method='POST',
                request_path='/api/auth/mfa/verify',
                success=True,
                metadata={'remaining_codes': len(self.backup_codes)}
            )

            return True

        return False

    def is_device_trusted(self, fingerprint):
        """Check if device is trusted"""
        return fingerprint in self.trusted_device_fingerprints

    def trust_device(self, fingerprint):
        """Add device to trusted list"""
        if fingerprint not in self.trusted_device_fingerprints:
            self.trusted_device_fingerprints.append(fingerprint)
            self.save()


class OTPCode(TimeStampedModel):
    """
    One-Time Password codes for SMS/Email verification
    """
    CODE_TYPES = [
        ('login', 'Login Verification'),
        ('password_reset', 'Password Reset'),
        ('email_verification', 'Email Verification'),
        ('phone_verification', 'Phone Verification'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='otp_codes')
    code = models.CharField(max_length=10)
    code_type = models.CharField(max_length=50, choices=CODE_TYPES)

    # Delivery
    delivery_method = models.CharField(max_length=20)  # sms, email
    delivery_address = models.CharField(max_length=255)  # phone or email

    # Status
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    # Security
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)

    class Meta:
        db_table = 'otp_codes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'code_type', '-created_at']),
            models.Index(fields=['code', 'is_used']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.code_type} - {'Used' if self.is_used else 'Active'}"

    @classmethod
    def generate(cls, user, code_type, delivery_method, delivery_address, validity_minutes=10):
        """Generate new OTP code"""
        code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])

        return cls.objects.create(
            user=user,
            code=code,
            code_type=code_type,
            delivery_method=delivery_method,
            delivery_address=delivery_address,
            expires_at=datetime.now() + timedelta(minutes=validity_minutes)
        )

    def verify(self, code):
        """Verify OTP code"""
        self.attempts += 1
        self.save()

        if self.attempts > self.max_attempts:
            return False, "Maximum attempts exceeded"

        if self.is_used:
            return False, "Code already used"

        if self.expires_at < datetime.now():
            return False, "Code expired"

        if self.code != code:
            return False, "Invalid code"

        self.is_used = True
        self.used_at = datetime.now()
        self.save()

        return True, "Code verified successfully"
