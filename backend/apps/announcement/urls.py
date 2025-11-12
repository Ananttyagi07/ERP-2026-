"""
URL Configuration for announcement
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet, NewsViewSet, HolidayViewSet

app_name = 'announcement'

router = DefaultRouter()
router.register(r'notices', NoticeViewSet, basename='notices')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'holidays', HolidayViewSet, basename='holidays')

urlpatterns = [
    path('', include(router.urls)),
]
