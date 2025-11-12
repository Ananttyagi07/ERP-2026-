"""
URL Configuration for messaging
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

app_name = 'messaging'

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]
