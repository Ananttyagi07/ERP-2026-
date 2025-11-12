"""Students URL patterns"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StudentParentViewSet

app_name = 'students'

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'student-parents', StudentParentViewSet, basename='student-parent')

urlpatterns = [
    path('', include(router.urls)),
]
