"""
Views for asset_management
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Vendor, Store, AssetCategory, AssetItem, AssetPurchase, AssetIssue
from .serializers import (
    VendorListSerializer, VendorCreateSerializer, VendorDetailSerializer,
    StoreListSerializer, StoreCreateSerializer, StoreDetailSerializer,
    AssetCategoryListSerializer, AssetCategoryCreateSerializer, AssetCategoryDetailSerializer,
    AssetItemListSerializer, AssetItemCreateSerializer, AssetItemDetailSerializer,
    AssetPurchaseListSerializer, AssetPurchaseCreateSerializer, AssetPurchaseDetailSerializer,
    AssetIssueListSerializer, AssetIssueCreateSerializer, AssetIssueDetailSerializer,
)


class VendorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Vendor
    Provides CRUD operations for Vendor
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Vendor.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return VendorListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return VendorCreateSerializer
        return VendorDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class StoreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Store
    Provides CRUD operations for Store
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = Store.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return StoreListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return StoreCreateSerializer
        return StoreDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class AssetCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AssetCategory
    Provides CRUD operations for AssetCategory
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = AssetCategory.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return AssetCategoryListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AssetCategoryCreateSerializer
        return AssetCategoryDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class AssetItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AssetItem
    Provides CRUD operations for AssetItem
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = AssetItem.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return AssetItemListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AssetItemCreateSerializer
        return AssetItemDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class AssetPurchaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AssetPurchase
    Provides CRUD operations for AssetPurchase
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = AssetPurchase.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return AssetPurchaseListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AssetPurchaseCreateSerializer
        return AssetPurchaseDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()


class AssetIssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AssetIssue
    Provides CRUD operations for AssetIssue
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by college for multi-tenancy"""
        queryset = AssetIssue.objects.filter(is_deleted=False)

        # Filter by college if user is not superadmin
        if hasattr(self.request.user, 'college') and self.request.user.college:
            queryset = queryset.filter(college=self.request.user.college)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return AssetIssueListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AssetIssueCreateSerializer
        return AssetIssueDetailSerializer

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_deleted = True
        instance.save()

