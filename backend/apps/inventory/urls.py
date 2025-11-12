from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SupplierViewSet, WarehouseViewSet, InventoryCategoryViewSet,
    ProductViewSet, PurchaseViewSet, SaleViewSet, ProductIssueViewSet
)

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'categories', InventoryCategoryViewSet, basename='inventory-category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'purchases', PurchaseViewSet, basename='purchase')
router.register(r'sales', SaleViewSet, basename='sale')
router.register(r'issues', ProductIssueViewSet, basename='product-issue')

urlpatterns = [
    path('', include(router.urls)),
]
