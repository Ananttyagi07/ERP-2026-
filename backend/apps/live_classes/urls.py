"""Live Classes URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LiveClassTypeViewSet, LiveClassViewSet, AssignmentViewSet

app_name = 'live_classes'

router = DefaultRouter()
router.register(r'live-class-types', LiveClassTypeViewSet, basename='live-class-type')
router.register(r'live-classes', LiveClassViewSet, basename='live-class')
router.register(r'assignments', AssignmentViewSet, basename='assignment')

urlpatterns = [
    path('', include(router.urls)),
]
