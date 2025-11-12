"""Templates URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SMSTemplateViewSet, EmailTemplateViewSet

app_name = 'templates'

router = DefaultRouter()
router.register(r'sms-templates', SMSTemplateViewSet, basename='sms-template')
router.register(r'email-templates', EmailTemplateViewSet, basename='email-template')

urlpatterns = [
    path('', include(router.urls)),
]
