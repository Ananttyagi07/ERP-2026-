"""
URL Configuration for frontend_cms
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FrontendPageViewSet, SliderViewSet, AboutSchoolViewSet

app_name = 'frontend_cms'

router = DefaultRouter()
router.register(r'frontend-pages', FrontendPageViewSet, basename='frontend-pages')
router.register(r'sliders', SliderViewSet, basename='sliders')
router.register(r'about-school', AboutSchoolViewSet, basename='about-school')

urlpatterns = [
    path('', include(router.urls)),
]
