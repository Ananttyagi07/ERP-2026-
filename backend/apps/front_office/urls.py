"""Front Office URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (VisitorPurposeViewSet, VisitorInfoViewSet, CallLogViewSet,
                    PostalDispatchViewSet, PostalReceiveViewSet)

app_name = 'front_office'

router = DefaultRouter()
router.register(r'visitor-purposes', VisitorPurposeViewSet, basename='visitor-purpose')
router.register(r'visitor-info', VisitorInfoViewSet, basename='visitor-info')
router.register(r'call-logs', CallLogViewSet, basename='call-log')
router.register(r'postal-dispatches', PostalDispatchViewSet, basename='postal-dispatch')
router.register(r'postal-receives', PostalReceiveViewSet, basename='postal-receive')

urlpatterns = [
    path('', include(router.urls)),
]
