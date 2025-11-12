"""
URL Configuration for asset_management
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, StoreViewSet, AssetCategoryViewSet, AssetItemViewSet, AssetPurchaseViewSet, AssetIssueViewSet

app_name = 'asset_management'

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendors')
router.register(r'stores', StoreViewSet, basename='stores')
router.register(r'asset-categories', AssetCategoryViewSet, basename='asset-categories')
router.register(r'asset-items', AssetItemViewSet, basename='asset-items')
router.register(r'asset-purchases', AssetPurchaseViewSet, basename='asset-purchases')
router.register(r'asset-issues', AssetIssueViewSet, basename='asset-issues')

urlpatterns = [
    path('', include(router.urls)),
]
