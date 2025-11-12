"""
URL Configuration for event
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet

app_name = 'event'

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
]
