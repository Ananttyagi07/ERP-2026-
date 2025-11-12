"""
URL Configuration for miscellaneous
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AwardViewSet, TodoViewSet, FAQViewSet

app_name = 'miscellaneous'

router = DefaultRouter()
router.register(r'awards', AwardViewSet, basename='awards')
router.register(r'todos', TodoViewSet, basename='todos')
router.register(r'faqs', FAQViewSet, basename='faqs')

urlpatterns = [
    path('', include(router.urls)),
]
