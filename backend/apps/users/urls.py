"""User Management URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserManagementViewSet, ResetPasswordView, ResetUsernameView, ViewCredentialsView

app_name = 'users'

router = DefaultRouter()
router.register(r'', UserManagementViewSet, basename='user')

urlpatterns = [
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('reset-username/', ResetUsernameView.as_view(), name='reset-username'),
    path('credentials/', ViewCredentialsView.as_view(), name='view-credentials'),
    path('', include(router.urls)),
]
