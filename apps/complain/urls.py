"""
URL Configuration for complain
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplainTypeViewSet, ComplainViewSet

app_name = 'complain'

router = DefaultRouter()
router.register(r'complain-types', ComplainTypeViewSet, basename='complain-types')
router.register(r'complains', ComplainViewSet, basename='complains')

urlpatterns = [
    path('', include(router.urls)),
]
