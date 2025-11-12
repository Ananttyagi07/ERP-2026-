"""Superadmin URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuperAdminViewSet

app_name = 'superadmin'

router = DefaultRouter()
router.register(r'superadmins', SuperAdminViewSet, basename='superadmin')

urlpatterns = [
    path('', include(router.urls)),
]
