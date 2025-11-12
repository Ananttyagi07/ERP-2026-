"""Guardians URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuardianViewSet

app_name = 'guardians'

router = DefaultRouter()
router.register(r'guardians', GuardianViewSet, basename='guardian')

urlpatterns = [
    path('', include(router.urls)),
]
