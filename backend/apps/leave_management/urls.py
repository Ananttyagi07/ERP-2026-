"""Leave Management URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveTypeViewSet, LeaveApplicationViewSet

app_name = 'leave_management'

router = DefaultRouter()
router.register(r'leave-types', LeaveTypeViewSet, basename='leave-type')
router.register(r'leave-applications', LeaveApplicationViewSet, basename='leave-application')

urlpatterns = [
    path('', include(router.urls)),
]
