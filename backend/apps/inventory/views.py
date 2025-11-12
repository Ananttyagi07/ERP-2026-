"""
Inventory Management views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Supplier, Warehouse, InventoryCategory, Product, Purchase, Sale, ProductIssue
from .serializers import *


class SupplierViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Supplier.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SupplierListSerializer
        elif self.action in ['create', 'update']:
            return SupplierCreateSerializer
        return SupplierDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class WarehouseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Warehouse.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WarehouseListSerializer
        elif self.action in ['create', 'update']:
            return WarehouseCreateSerializer
        return WarehouseDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class InventoryCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = InventoryCategory.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return InventoryCategoryListSerializer
        elif self.action in ['create', 'update']:
            return InventoryCategoryCreateSerializer
        return InventoryCategoryDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update']:
            return ProductCreateSerializer
        return ProductDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college)


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Purchase.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PurchaseListSerializer
        elif self.action in ['create', 'update']:
            return PurchaseCreateSerializer
        return PurchaseDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, purchased_by=self.request.user)


class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Sale.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SaleListSerializer
        elif self.action in ['create', 'update']:
            return SaleCreateSerializer
        return SaleDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, sold_by=self.request.user)


class ProductIssueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProductIssue.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductIssueListSerializer
        elif self.action in ['create', 'update']:
            return ProductIssueCreateSerializer
        return ProductIssueDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college, is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(college=self.request.user.college, issued_by=self.request.user)
