"""
Authentication URL patterns
"""
from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RefreshTokenView,
    MyPermissionsView,
    MyProfileView,
    VerifyTokenView
)
from .views_security import (
    EnhancedLoginView,
    EnhancedLogoutView,
    MFAVerifyView,
    SessionListView,
    SessionRevokeView,
    SessionRevokeAllView
)
from .views_mfa import (
    MFAStatusView,
    MFASetupInitiateView,
    MFASetupCompleteView,
    MFADisableView,
    MFARegenerateBackupCodesView,
    MFATrustedDevicesView,
    MFARemoveTrustedDeviceView
)

app_name = 'authentication'

urlpatterns = [
    # Basic authentication endpoints (backwards compatibility)
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh-token'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify-token'),

    # Enhanced enterprise authentication endpoints
    path('login/secure/', EnhancedLoginView.as_view(), name='enhanced-login'),
    path('logout/secure/', EnhancedLogoutView.as_view(), name='enhanced-logout'),

    # MFA verification endpoint
    path('mfa/verify/', MFAVerifyView.as_view(), name='mfa-verify'),

    # MFA setup and management endpoints
    path('mfa/status/', MFAStatusView.as_view(), name='mfa-status'),
    path('mfa/setup/initiate/', MFASetupInitiateView.as_view(), name='mfa-setup-initiate'),
    path('mfa/setup/complete/', MFASetupCompleteView.as_view(), name='mfa-setup-complete'),
    path('mfa/disable/', MFADisableView.as_view(), name='mfa-disable'),
    path('mfa/backup-codes/regenerate/', MFARegenerateBackupCodesView.as_view(), name='mfa-regenerate-codes'),
    path('mfa/trusted-devices/', MFATrustedDevicesView.as_view(), name='mfa-trusted-devices'),
    path('mfa/trusted-devices/<str:fingerprint>/', MFARemoveTrustedDeviceView.as_view(), name='mfa-remove-device'),

    # Session management endpoints
    path('sessions/', SessionListView.as_view(), name='session-list'),
    path('sessions/<str:session_id>/', SessionRevokeView.as_view(), name='session-revoke'),
    path('sessions/revoke-all/', SessionRevokeAllView.as_view(), name='session-revoke-all'),

    # User information endpoints
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),
    path('my-permissions/', MyPermissionsView.as_view(), name='my-permissions'),
]
