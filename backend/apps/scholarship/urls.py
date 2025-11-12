"""
URL Configuration for scholarship
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScholarshipCandidateViewSet, DonorViewSet, ScholarshipViewSet

app_name = 'scholarship'

router = DefaultRouter()
router.register(r'scholarship-candidates', ScholarshipCandidateViewSet, basename='scholarship-candidates')
router.register(r'donors', DonorViewSet, basename='donors')
router.register(r'scholarships', ScholarshipViewSet, basename='scholarships')

urlpatterns = [
    path('', include(router.urls)),
]
