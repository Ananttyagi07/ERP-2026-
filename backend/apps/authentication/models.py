"""
Authentication models for token management
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
import secrets


class RefreshToken(TimeStampedModel):
    """
    Opaque refresh tokens stored in database
    Used for token rotation and blacklisting
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='refresh_tokens'
    )
    token = models.CharField(max_length=255, unique=True, db_index=True)
    expires_at = models.DateTimeField()
    is_revoked = models.BooleanField(default=False)

    # Device/session tracking
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    # Token rotation tracking
    replaced_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replaced_token'
    )

    class Meta:
        db_table = 'refresh_tokens'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token', 'is_revoked']),
            models.Index(fields=['user', 'is_revoked']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.token[:20]}..."

    @classmethod
    def generate_token(cls):
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)

    def revoke(self):
        """Revoke this refresh token"""
        self.is_revoked = True
        self.save(update_fields=['is_revoked'])


class BlacklistedToken(TimeStampedModel):
    """
    Blacklist for revoked JWT access tokens
    Used for immediate token revocation before expiry
    """
    token = models.CharField(max_length=500, unique=True, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blacklisted_tokens'
    )
    expires_at = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'blacklisted_tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f"Blacklisted: {self.user.email}"


# Import enterprise security models
from .models_security import (
    SecurityAuditLog,
    UserSession,
    UserMFA,
    OTPCode
)

__all__ = [
    'RefreshToken',
    'BlacklistedToken',
    'SecurityAuditLog',
    'UserSession',
    'UserMFA',
    'OTPCode',
]
