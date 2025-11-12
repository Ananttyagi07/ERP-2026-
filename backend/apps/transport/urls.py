"""
URL Configuration for transport
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, TransportRouteViewSet, RouteStopViewSet, TransportMemberViewSet

app_name = 'transport'

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicles')
router.register(r'routes', TransportRouteViewSet, basename='routes')
router.register(r'route-stops', RouteStopViewSet, basename='route-stops')
router.register(r'transport-members', TransportMemberViewSet, basename='transport-members')

urlpatterns = [
    path('', include(router.urls)),
]
