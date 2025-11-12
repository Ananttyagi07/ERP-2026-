from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IDCardSettingViewSet, AdmitCardSettingViewSet

router = DefaultRouter()
router.register(r'id-card-settings', IDCardSettingViewSet, basename='id-card-setting')
router.register(r'admit-card-settings', AdmitCardSettingViewSet, basename='admit-card-setting')

urlpatterns = [
    path('', include(router.urls)),
]
