"""
URL Configuration for media_gallery
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GalleryViewSet, GalleryImageViewSet

app_name = 'media_gallery'

router = DefaultRouter()
router.register(r'galleries', GalleryViewSet, basename='galleries')
router.register(r'gallery-images', GalleryImageViewSet, basename='gallery-images')

urlpatterns = [
    path('', include(router.urls)),
]
