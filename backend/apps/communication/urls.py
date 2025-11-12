"""
URL Configuration for communication
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailLogViewSet, SMSLogViewSet

app_name = 'communication'

router = DefaultRouter()
router.register(r'email-logs', EmailLogViewSet, basename='email-logs')
router.register(r'sms-logs', SMSLogViewSet, basename='sms-logs')

urlpatterns = [
    path('', include(router.urls)),
]
